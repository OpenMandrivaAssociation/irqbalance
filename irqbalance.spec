Summary:	Daemon to balance irq's across multiple CPUs
Name:		irqbalance
Version:	1.0.6
Release:	5
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://irqbalance.org/
Source0:	http://irqbalance.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:	%{name}.sysconfig
BuildRequires:	gccmakedep
%ifnarch %arm
BuildRequires	numa-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcap-ng)
Requires(post,preun):	rpm-helper

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q
# (tpg) for new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*

# (tpg) fix path
sed -i 's|EnvironmentFile=.*|EnvironmentFile=/etc/sysconfig/irqbalance|' misc/irqbalance.service

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service

%post
%_post_service irqbalance

%preun
%_preun_service irqbalance


%files
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/sysconfig/*
%{_sbindir}/*
%{_unitdir}/%{name}.service
%{_mandir}/man1/*
