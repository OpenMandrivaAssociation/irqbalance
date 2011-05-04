Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	0.56
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://irqbalance.org/
Source0:	http://irqbalance.googlecode.com/files/%{name}-%{version}.tbz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	irqbalance.1
Requires(post,preun):		rpm-helper
BuildRequires:	gccmakedep
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
touch NEWS README AUTHORS ChangeLog

%build
./autogen.sh

%configure2_5x
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man1}
install irqbalance %{buildroot}%{_sbindir}
mkdir -p %{buildroot}{%{_initrddir},%{_sysconfdir}/sysconfig}
install %{SOURCE1} %{buildroot}%{_initrddir}/irqbalance
install %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/irqbalance
install %{SOURCE3} %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_sbindir}/*
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
