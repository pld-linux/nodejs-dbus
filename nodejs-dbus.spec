#
# Conditional build:
%bcond_without	tests		# build without tests

%define		pkg	dbus
Summary:	D-Bus binding for node.js
Name:		nodejs-%{pkg}
Version:	0.0.10
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/dbus/-/%{pkg}-%{version}.tgz
# Source0-md5:	6af3be618225f5596bd9778ebd90b85a
Patch0:		load-native.patch
URL:		https://github.com/Shouqun/node-dbus
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	expat-devel
BuildRequires:	nodejs >= 0.8
BuildRequires:	nodejs-devel
BuildRequires:	nodejs-gyp
BuildRequires:	rpmbuild(macros) >= 1.657
BuildRequires:	sed >= 4.0
Requires:	nodejs >= 0.8
Requires:	nodejs-gcontext >= 0.0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# redefine for arch specific
%define		nodejs_libdir %{_libdir}/node

%description
D-Bus binding for node.js.

Has the following capabilities:
- call D-Bus methods
- asynchronous method call
- receive D-Bus signals
- export D-Bus services

%prep
%setup -qc
mv package/* .
%patch0 -p1

rm lib/.travis.yml

%build
node-gyp configure --nodedir=/usr/src/nodejs --gyp=/usr/bin/gyp
node-gyp build --jobs=%{?__jobs} --verbose

%if %{with tests}
node -e 'require("./build/Release/%{pkg}")'
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr lib package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
install -p build/Release/%{pkg}.node $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Readme.md
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%dir %{nodejs_libdir}/%{pkg}/lib
%{nodejs_libdir}/%{pkg}/lib/dbus.js
%{nodejs_libdir}/%{pkg}/lib/dbus_register.js
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/%{pkg}.node
%{_examplesdir}/%{name}-%{version}
