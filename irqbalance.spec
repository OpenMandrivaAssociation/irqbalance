Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	0.55
Release:	%mkrel 9
License:	GPLv2+
Group:		System/Kernel and hardware
URL:            http://irqbalance.org/
Source0:	http://www.irqbalance.org/releases/%name-%version.tar.bz2
Source1:	%name.init
Source2:	%name.sysconfig
Source3:	irqbalance.1
# Fedora patches:
Patch0: irqbalance-pie.patch
Patch1: irqbalance-0.55-cputree-parse.patch
Patch2: irqbalance-0.55-pid-file.patch
# (fc) 0.55-8mdv enable libcap-ng support (Fedora)
Patch3: irqbalance-0.55-config-capng.patch
BuildRoot:      %_tmppath/%name-%version-buildroot
Requires(post,preun):		rpm-helper
BuildRequires: gccmakedep
BuildRequires: glib2-devel
BuildRequires: libcap-ng-devel

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q 

#%patch0 -p1
%patch1 -p1
%patch2 -p2
%patch3 -p1 -b .libcap-ng

#needed by patch3
touch NEWS README AUTHORS ChangeLog
autoreconf -i

%build
%configure
%make


%install
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi

mkdir -p $RPM_BUILD_ROOT{%_sbindir,%_mandir/man1}
install irqbalance $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT{%{_initrddir},%{_sysconfdir}/sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/irqbalance
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/irqbalance
install %{SOURCE3} %{buildroot}%_mandir/man1/

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi


%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%defattr(-,root,root)
%_mandir/man1/*
%_sbindir/*
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
