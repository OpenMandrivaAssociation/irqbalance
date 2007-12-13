Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	0.55
Release:	%mkrel 3
License:	Open Software License
Group:		System/Kernel and hardware
URL:            http://irqbalance.org/
Source0:	http://www.irqbalance.org/releases/%name-%version.tar.bz2
Source1:	%name.init
Source2:	%name.sysconfig
BuildRoot:      %_tmppath/%name-%version-buildroot
Requires(post,preun):		rpm-helper
BuildRequires: 	gccmakedep glib2-devel

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q

%build
%make


%install
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install irqbalance $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT{%{_initrddir},%{_sysconfdir}/sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/irqbalance
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/irqbalance

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi


%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%defattr(-,root,root)
%_sbindir/*
%config(noreplace) %{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
