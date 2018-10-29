%define _disable_ld_no_undefined 1

Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.5.0
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://irqbalance.org/
Source0:	https://codeload.github.com/Irqbalance/irqbalance/tar.gz/%{name}-%{version}.tar.gz
Source1:	%{name}.sysconfig
BuildRequires:	gccmakedep
BuildRequires:	pkgconfig(ncursesw)
%ifnarch %{armx}
BuildRequires:	numa-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcap-ng)
%if %mdvver < 3000000
BuildRequires:	pkgconfig(libsystemd-journal)
%else
BuildRequires:	pkgconfig(libsystemd)
%endif

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%files
%doc AUTHORS
%{_mandir}/man1/*
%{_sbindir}/*
%{_systemunitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/*

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches
%if %mdvver < 3000000
# (tpg) fix build with older systemd
sed -i -e "s#AC_CHECK_LIB(\[systemd\]#AC_CHECK_LIB(\[libsystemd-journal\]#g" configure.ac
%endif

./autogen.sh

# (tpg) fix path
sed -i 's|EnvironmentFile=.*|EnvironmentFile=/etc/sysconfig/irqbalance|' misc/irqbalance.service

%build
%if %mdvver < 3000000
%global optflags %optflags -std=c99
%endif

%configure \
	--disable-static \
	--with-systemd

%if %mdvver < 3000000
%make CFLAGS="%{optflags} $(pkg-config --cflags libsystemd-journal) $(pkg-config --libs libsystemd-journal)" LDFLAGS="%{ldflags} $(pkg-config --libs libsystemd-journal)"
%else
%make_build
%endif

%install
sed -ie "s|^EnvironmentFile=.*|EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}|g" misc/irqbalance.service
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
