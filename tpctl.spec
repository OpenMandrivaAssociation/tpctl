%define major	2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Thinkpad Utilities
Name:		tpctl
Version:	4.17
Release:	14
URL:		http://tpctl.sourceforge.net/
Group:		System/Kernel and hardware
License:	GPLv2
Source0:	http://prdownloads.sourceforge.net/tpctl/%{name}_%{version}.tar.gz
Source1:	apmiser.init.bz2
Source2:	hdparm-contrib-ultrabayd.tar.bz2
Source3:	ultrabayd.init.bz2
Source4:	ultrabay.suspend.bz2
Patch0:		hdparm-5.4-fix_path_bell_idectl.patch
Patch1:		tpctl-4.17_ncurses.patch
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	pkgconfig(ncurses)
Requires:	hdparm

%description
Utilities specific to IBM Thinkpads

%package -n %{libname}
Summary:	Library associated with tpctl, needed for tpctl utilities
Group:		System/Libraries

%description -n	%{libname}
This library is mandatory for tpctl utilities.
 
%package -n	%{devname}
Summary:	Development package with static libs and headers
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{_lib}tpctl2-devel < 4.17-12

%description -n	%{devname}
This package contains header files and static library for tpctl
utilities.
 
%prep
%setup -q -a 2
# 4.4-2mdk (Abel) needs Source2
%apply_patches
mv contrib/README contrib/idectl-README

# stupid makefile
perl -pi -e "s|-o 0 -g 0||g" Makefile

%build
%make PATH_LIB=%_libdir/

%install
mkdir -p %{buildroot}/{%{_sbindir},%{_mandir}/man1}
make install DEST=%{buildroot} PATH_LIB=%_libdir/

cd %{buildroot}/%{_libdir}/
ln -sf libsmapidev.so.2.0 libsmapidev.so 
cd -
mkdir -p %{buildroot}/%{_initrddir}
bzcat %{SOURCE1} > %{buildroot}/%{_initrddir}/apmiser
chmod 755 %{buildroot}/%{_initrddir}/apmiser

mkdir -p %{buildroot}/%{_includedir}
cp -r include %{buildroot}/%{_includedir}/%{name}

mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 man/apmiser.8 %{buildroot}/%{_mandir}/man8/

# 4.4-2mdk (Abel) ultrabayd stuff
install -m 0755 contrib/idectl %{buildroot}/%{_sbindir}/idectl
install -m 0755 contrib/ultrabayd %{buildroot}/%{_sbindir}/ultrabayd
bzcat %{SOURCE3} > %{buildroot}%{_initrddir}/ultrabayd
chmod 755 %{buildroot}%{_initrddir}/ultrabayd
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/suspend-scripts/suspend.d/
bzcat %{SOURCE4} > %{buildroot}%{_sysconfdir}/sysconfig/suspend-scripts/suspend.d/ultrabay
chmod 755 %{buildroot}%{_sysconfdir}/sysconfig/suspend-scripts/suspend.d/ultrabay

%files
%doc AUTHORS COPYING README SUPPORTED-MODELS TROUBLESHOOTING VGA-MODES
%doc contrib/idectl-README
%config(noreplace) %{_sysconfdir}/sysconfig/suspend-scripts/suspend.d/*
%{_initrddir}/*
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*

