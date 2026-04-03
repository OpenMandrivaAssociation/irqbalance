%define _disable_ld_no_undefined 1
%undefine _debugsource_packages

Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.9.5
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		https://irqbalance.org/
Source0:	https://github.com/Irqbalance/irqbalance/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.sysconfig
Source2:	%{name}.tmpfiles
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	make
BuildRequires:	slibtool
BuildRequires:	gccmakedep
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	libtool-autoconf-macros
%ifnarch %{armx} riscv64
BuildRequires:	numa-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros

%patchlist
irqbalance-1.9.5-fix-unit-file.patch

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

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
sed -i 's|EnvironmentFile=.*|EnvironmentFile=-/etc/sysconfig/irqbalance|' misc/irqbalance.service.in

%build
%configure \
	--disable-static \
	--with-systemd

%make_build

%install
%make_install
#install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
#install -d %{buildroot}%{_mandir}/man1/
#install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/
#install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
# Remove debianisms
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}
# Add configs
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d %{buildroot}%{_presetdir}

cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF
