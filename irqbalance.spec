Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.0.5
Release:	2
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://irqbalance.org/
Source0:	http://irqbalance.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:	%{name}.sysconfig
Requires(post,preun):	rpm-helper
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
# (tpg) for new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*

# (tpg) fix path
sed -i 's|EnvironmentFile=.*|EnvironmentFile=/etc/sysconfig/irqbalance|' misc/irqbalance.service

%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

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
