Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.0.3
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
BuildRequires:	glib2-devel
%if %mdkversion >= 201010
BuildRequires:	libcap-ng-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
rm -rf %{buildroot}
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/

%if %mdkver >= 201100
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
%else
mkdir -p %{buildroot}%{_initrddir}
install %{SOURCE1} %{buildroot}%{_initrddir}/irqbalance
%endif

%clean
rm -rf %{buildroot}

%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%defattr(-,root,root)
%doc AUTHORS
%{_mandir}/man1/*
%{_sbindir}/*
%if %mdkver >= 201100
%{_unitdir}/%{name}.service
%else
%{_initrddir}/*
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/*
