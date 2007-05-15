%define name	irqbalance
%define version	0.55
%define release	%mkrel 1


Summary:	Daemon to balance irq's across multiple CPUs.
Name:		%name
Version:	%version
Release:	%release
License:	Open Software License
Group:		System/Kernel and hardware
URL:            http://people.redhat.com/arjanv/irqbalance/
Source0:        %name-%version.tar.bz2
Source1:	%name.init
Source2:	%name.sysconfig
BuildRoot:      %_tmppath/%name-%version-buildroot
PreReq:		rpm-helper
BuildRequires: 	gccmakedep

%description
Daemon to balance irq's across multiple CPUs on systems with
the 2.4 or 2.6 kernel. Only useful on SMP systems.

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
