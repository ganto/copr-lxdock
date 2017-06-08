%global         with_python3 1

Name:		    python-dotenv
Version:	    0.0.5
Release:	    1%{?dist}
Summary:	    Python .env file handler

License:	    MIT
URL:		    https://pypi.python.org/pypi/dotenv
Source0:	    https://files.pythonhosted.org/packages/source/d/dotenv/dotenv-%{version}.tar.gz
Patch0:         dotenv-0.0.5-No-setup_requires-of-distribute.patch
Patch1:         dotenv-0.0.5-fixed-typo-in-sample-code.patch
BuildArch:      noarch

%description
Shell Command and Library to write and read .env like files.

# don't try to build debug package
%global debug_package %{nil}

%package -n python2-dotenv
Summary:        %{summary}

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

%description -n python2-dotenv

%if 0%{?with_python3}
%package -n python3-dotenv
Summary:        Python 3 .env file handler

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose

%description -n python3-dotenv
%endif # with_python3

%package -n dotenv
Summary:        Script to parse .env file

Requires:       bash
Requires:       ((python2-dotenv = %{version}-%{release} if python) or python3-dotenv = %{version}-%{release})  

%description -n dotenv
Simple Python script to query a .env file with help of the dotenv
module.

%prep
%autosetup -n dotenv-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root %{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install --root %{buildroot}
%endif # with_python3
 
%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3

%files -n python2-dotenv
%doc README.md
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-dotenv
%doc README.md
%{python3_sitelib}/*
%endif # with_python3

%files -n dotenv
/usr/bin/dotenv

%changelog
* Thu Jun 08 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.0.5-1
- New package built with tito

