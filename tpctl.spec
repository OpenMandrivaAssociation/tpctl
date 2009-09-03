%define lib_major 2
%define libname %mklibname %{name} %{lib_major}

Summary:	Thinkpad Utilities
Name:		tpctl
Version:	4.17
Release:	%mkrel 6
URL:		http://tpctl.sourceforge.net/
Group:		System/Kernel and hardware
License:	GPL
ExclusiveArch:	%{ix86}
Source:		http://prdownloads.sourceforge.net/tpctl/%{name}_%{version}.tar.gz
Source1:	apmiser.init.bz2
Source2:	hdparm-contrib-ultrabayd.tar.bz2
Source3:	ultrabayd.init.bz2
Source4:	ultrabay.suspend.bz2
Patch0:		hdparm-5.4-fix_path_bell_idectl.patch
BuildRequires:	ncurses-devel
Requires:	%{libname} = %{version}-%{release}
#Requires(post): rpm-helper
#Requires(preun): rpm-helper
# 4.4-2mdk (Abel) idectl and ultrabayd is moved to this package
Requires:	hdparm >= 5.4-3mdk
Conflicts:	hdparm <= 5.4-2mdk
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Utilities specific to IBM Thinkpads

%package -n %{libname}
Summary:	Library associated with tpctl, needed for tpctl utilities
Group:		System/Libraries

%description -n	%{libname}
This library is mandatory for tpctl utilities.
 
%package -n	%{libname}-devel
Summary:	Development package with static libs and headers
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 

%description -n	%{libname}-devel
This package contains header files and static library for tpctl
utilities.
 
%prep

%setup -q -a 2
# 4.4-2mdk (Abel) needs Source2
%patch0 -p1 -b .ultrabay
mv contrib/README contrib/idectl-README

# stupid makefile
perl -pi -e "s|-o 0 -g 0||g" Makefile

%build
make CFLAGS="%{optflags}" all

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_sbindir},%{_mandir}/man1}
make install DEST=%{buildroot}

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

%clean
rm -rf %{buildroot}

#post 
#_post_service apmiser
#_post_service ultrabayd

#preun 
#_preun_service apmiser
#_preun_service ultrabayd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README SUPPORTED-MODELS TROUBLESHOOTING VGA-MODES
%doc contrib/idectl-README
%config(noreplace) %{_sysconfdir}/sysconfig/suspend-scripts/suspend.d/*
%{_initrddir}/*
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man?/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc ChangeLog COPYING 
%{_libdir}/*.so
%{_includedir}/*
