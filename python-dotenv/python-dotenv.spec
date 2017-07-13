%global         with_python3 1

Name:           python-dotenv
Version:        0.6.4
Release:        1%{?dist}
Summary:        Python .env file handler

License:        BSD
URL:            https://github.com/theskumar/python-dotenv
Source0:        https://github.com/theskumar/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
BuildArch:      noarch

%description
Reads the key,value pair from '.env' and adds them to environment
variable.

# don't try to build debug package
%global debug_package %{nil}

%package -n python2-dotenv
Summary:        %{summary}

Requires:       python-click >= 5.0

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-click >= 5.0
BuildRequires:  python-pytest
BuildRequires:  python-sh

%description -n python2-dotenv
Python 2 library to read the key,value pair from '.env' and adds them
to environment variable.

%if 0%{?with_python3}
%package -n python3-dotenv
Summary:        Python 3 .env file handler

Requires:       python3-click >= 5.0

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-click >= 5.0
BuildRequires:  python3-pytest
BuildRequires:  python3-sh

%description -n python3-dotenv
Python 3 library to read the key,value pair from '.env' and adds them
to environment variable.
%endif # with_python3

%package -n dotenv
Summary:        Script to parse .env file

Requires:       python3-dotenv = %{version}-%{release}

%description -n dotenv
CLI interface which helps you manipulate the '.env' file without manually
opening it.

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT
%py2_install
%if 0%{?with_python3}
%py3_install
%endif # with_python3
 
%check
# cannot run cli test from source directory
py.test -v --ignore=tests/test_cli.py
%if 0%{?with_python3}
py.test-3 -v --ignore=tests/test_cli.py
%endif # with_python3

%files -n python2-dotenv
%license LICENSE
%doc README.rst
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-dotenv
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%endif # with_python3

%files -n dotenv
%license LICENSE
/usr/bin/dotenv

%changelog
* Thu Jun 08 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.0.5-1
- New package built with tito

