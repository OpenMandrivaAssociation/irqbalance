%define _disable_ld_no_undefined 1

Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.9.3
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://irqbalance.org/
Source0:	https://codeload.github.com/Irqbalance/irqbalance/tar.gz/%{name}-%{version}.tar.gz
Source1:	%{name}.sysconfig
Source2:	%{name}.tmpfiles
BuildRequires:	gccmakedep
BuildRequires:	pkgconfig(ncursesw)
%ifnarch %{armx} riscv64
BuildRequires:	numa-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc AUTHORS
%doc %{_mandir}/man1/*
%{_sbindir}/*
%{_presetdir}/86-%{name}.preset
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1
./autogen.sh

# (tpg) fix path
sed -i 's|EnvironmentFile=.*|EnvironmentFile=-/etc/sysconfig/irqbalance|' misc/irqbalance.service

%build
%configure \
	--disable-static \
	--with-systemd

%make_build

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d %{buildroot}%{_presetdir}

cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF
