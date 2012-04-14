#
# Conditional build:
%bcond_without	tests		# build without tests

%define		pkg	dbus
Summary:	D-Bus binding for node.js
Name:		nodejs-%{pkg}
Version:	0.0.4
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/Shouqun/node-dbus
Source0:	http://registry.npmjs.org/dbus/-/%{pkg}-%{version}.tgz
# Source0-md5:	1a31a9aca3367897684a491a548d1f08
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	expat-devel
BuildRequires:	nodejs-devel
BuildRequires:	rpmbuild(macros) >= 1.634
Requires:	nodejs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		nodejs_libdir %{_libdir}/node

%description
D-Bus binding for node.js.

Has the following capabilities:
- call D-Bus methods
- receive D-Bus signals
- export D-Bus services

%prep
%setup -qc
mv package/* .

%build
NODE_PATH=%{nodejs_libdir}/%{pkg} \
node-waf configure build

%if %{with tests}
NODE_PATH=lib node -e 'require("%{pkg}")'
%endif

%install
rm -rf $RPM_BUILD_ROOT
node-waf install \
	--destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -a lib package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

# waf installed to wrong dir
rm $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}/dbus.node

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
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/lib/%{pkg}.node
