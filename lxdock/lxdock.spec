%global pkgname lxdock
%global with_check 0

# don't try to build debug package
%global debug_package %{nil}

%define compdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{compdir}" == ""
%define compdir "/etc/bash_completion.d"
%endif

Name:           %{pkgname}
Version:        0.3.0
Release:        2%{?dist}
Summary:        LXDock is a tool for orchestrating LXD containers

Group:          Development/Languages
License:        GPLv3
URL:            https://lxdock.readthedocs.io/
Source0:        https://github.com/lxdock/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  bash-completion

Requires:       python3-%{pkgname} = %{version}-%{release}

%description
%{summary}.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation

BuildRequires:  python3-sphinx

%description    doc
Documentation for %{name}.

%package -n python3-%{pkgname}
Summary:        Python 3 module of LXDock

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-colorlog
BuildRequires:  python3-dotenv >= 0.6
BuildRequires:  python3-isort
BuildRequires:  python3-pylxd >= 2.2.4
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-spec
BuildRequires:  python3-PyYAML >= 3.0
BuildRequires:  python3-requests >= 2.5.1
BuildRequires:  python3-voluptuous >= 0.9
%endif

Requires:       python3-colorlog
Requires:       python3-dotenv >= 0.6
Requires:       python3-pylxd >= 2.2.4
Requires:       python3-PyYAML >= 3.0
Requires:       python3-requests >= 2.5.1
Requires:       python3-voluptuous >= 0.9

%description -n python3-%{pkgname}
Python 3 module of LXDock.

%package -n python3-%{pkgname}-tests
Summary:        Tests for the lxdock Python 3 library.

Requires:       python3-%{pkgname} = %{version}-%{release}
Requires:       python3-isort
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-pytest-spec

%description -n python3-%{pkgname}-tests
Tests for the LXDock Python 3 module.

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py3_build
pushd docs
%{__make} html
popd

%install
%py3_install
# bash-completion
%{__install} -d %{buildroot}%{compdir}
%{__install} -p -m 0644 contrib/completion/bash/%{pkgname} %{buildroot}%{compdir}
# zsh-completion
%{__install} -d %{buildroot}%{_datadir}/zsh/site-functions
%{__install} -p -m 0644 contrib/completion/zsh/_%{pkgname} %{buildroot}%{_datadir}/zsh/site-functions
# Fix hidden-file-or-dir warnings
rm -fr docs/_build/html/.buildinfo

%if 0%{?with_check}
%check
# TODO: extend and fix tests
py.test-3 lxdock
%endif

%files
%doc CHANGELOG.rst CONTRIBUTING.rst README.rst
%license LICENSE
%{_bindir}/lxdock
%(dirname %{compdir})
%{_datadir}/zsh/site-functions

%files doc
%doc docs/_build/html
%license LICENSE

%files -n python3-%{pkgname}
%license LICENSE
%{python3_sitelib}/*
%exclude %{python3_sitelib}/tests
%exclude %{python3_sitelib}/%{pkgname}/test

# TODO: fix test package
%files -n python3-%{pkgname}-tests
%license LICENSE
%{python3_sitelib}/%{pkgname}/test

%changelog
* Thu Jul 13 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3.0-2
- Fix python-dotenv dependency specification

* Wed Jul 12 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.3.0-1
- Version bump to release 0.3.0

* Tue Jun 13 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.2.1-1
- new package built with tito

