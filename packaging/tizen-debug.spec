#%define debug_package %{nil}
#%define __strip /bin/true

Name:		tizen-debug
Summary:	libc debug information with .debug_frame section only and ld debug information
Version:	2.20
Release:	1
License:	LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group:		Development/Libraries
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	glibc-debuginfo = %{version}
BuildRequires:	binutils

%description
The package contains the libc.so debug library with .debug_frame section only
which can be helpful during signal frame backtrace.
Also, the ld.so debug information is included for the debugging convenience.

%prep
%setup -q

%install
mkdir -p %{buildroot}/%{_prefix}/lib/debug/%{_lib}
objcopy -j .note.gnu.build-id -j .debug_frame %{_prefix}/lib/debug/%{_lib}/libc-%{version}-2014.11.so.debug %{buildroot}%{_prefix}/lib/debug/%{_lib}/libc-%{version}-2014.11.so.debug
cp %{_prefix}/lib/debug/%{_lib}/ld-%{version}-2014.11.so.debug %{buildroot}%{_prefix}/lib/debug/%{_lib}/ld-%{version}-2014.11.so.debug
chmod 444 %{buildroot}%{_prefix}/lib/debug/%{_lib}/*.so.debug
for file in %{buildroot}%{_prefix}/lib/debug/%{_lib}/ld-%{version}-2014.11.so.debug %{buildroot}%{_prefix}/lib/debug/%{_lib}/libc-%{version}-2014.11.so.debug; do
	BuildID=$(readelf -n $file | grep 'Build ID' | awk '{print $3}')
	Dir=$(echo $BuildID | cut -b-2)
	File=$(echo $BuildID | cut -b3-)
	mkdir -p %{buildroot}%{_prefix}/lib/debug/.build-id/$Dir
	cp -d %{_prefix}/lib/debug/.build-id/$Dir/$File.debug  %{buildroot}%{_prefix}/lib/debug/.build-id/$Dir
done

%files
%defattr(-,root,root)
%{_prefix}/lib/debug/%{_lib}/*.so.debug
%{_prefix}/lib/debug/.build-id/*
%manifest %{name}.manifest
