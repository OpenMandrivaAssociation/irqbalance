Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.1.0
Release:	2
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://irqbalance.org/
Source0:	https://codeload.github.com/Irqbalance/irqbalance/tar.gz/%{name}-%{version}.tar.gz
Source1:	%{name}.sysconfig
Patch0:		irqbalance-fix-aarch64.patch
BuildRequires:	gccmakedep
%ifnarch %{armx}
BuildRequires:	numa-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libsystemd-journal)

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%files
%doc AUTHORS
%{_mandir}/man1/*
%{_sbindir}/*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/*

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

./autogen.sh

# (tpg) fix path
sed -i 's|EnvironmentFile=.*|EnvironmentFile=/etc/sysconfig/irqbalance|' misc/irqbalance.service

%build
%configure \
	--disable-static \
	--with-systemd

%make

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
