Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.0.5
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://irqbalance.org/
Source0:	http://irqbalance.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	irqbalance.1
Requires(post,preun):		rpm-helper
BuildRequires:	gccmakedep
BuildRequires:	numa-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	libcap-ng-devel

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service

%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%doc AUTHORS
%{_mandir}/man1/*
%{_sbindir}/*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/*
