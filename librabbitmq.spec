%define revision 20120216
%define rabbitmq_c_hg_rev fb6fca832fd2
%define rabbitmq_codegen_hg_rev 6fb87d6eb01b
Summary: rabbitmq-c library
Name: librabbitmq
Version: 0.1
Release: %{revision}.1
License: GPL 2.0/MPL
Group: System Environment/Libraries
URL: http://hg.rabbitmq.com/rabbitmq-c/

Source0: rabbitmq-c-%{rabbitmq_c_hg_rev}.tar.bz2
Source1: rabbitmq-codegen-%{rabbitmq_codegen_hg_rev}.tar.bz2

Patch: librabbitmq-so.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: python-simplejson
BuildRequires: autoconf, make, popt-devel
BuildRequires: cmake >= 2.8.0

%description

%package        devel
Summary:        Development files for RabbitMQ-c
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for RabbitMQ.

%prep
%setup -q -n rabbitmq-c-%{rabbitmq_c_hg_rev}
%setup -D -T -a 1 -n rabbitmq-c-%{rabbitmq_c_hg_rev}

%patch -p1 

%build

mkdir bin-rabbitmq-c
cd bin-rabbitmq-c
cmake ../ -DRABBITMQ_CODEGEN_DIR=../rabbitmq-codegen-%{rabbitmq_codegen_hg_rev} -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT%{_usr} -DCMAKE_BUILD_TYPE=Release -DIMPORT_SUFFIX=so.lol

make

%install
rm -rf $RPM_BUILD_ROOT

cd bin-rabbitmq-c
make install

if [ "$RPM_BUILD_ROOT/usr/lib" != "$RPM_BUILD_ROOT%{_libdir}" ] ; then
	 mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/%{_libdir}
fi

ln -sf %{_libdir}/librabbitmq.so.0.1 $RPM_BUILD_ROOT%{_libdir}/librabbitmq.so.0
ln -sf %{_libdir}/librabbitmq.so.0.1 $RPM_BUILD_ROOT%{_libdir}/librabbitmq.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Fri Feb 17 2012 Taneli Leppa <taneli@crasman.fi> - 
- Initial build.

