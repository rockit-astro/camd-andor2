Name:      observatory-andor-camera-client
Version:   20220722
Release:   0
Url:       https://github.com/warwick-one-metre/camd
Summary:   Control client for Andor CCD cameras.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3 python3-Pyro4 python3-warwick-observatory-common python3-warwick-observatory-andor-camera

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/cam %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/cam %{buildroot}/etc/bash_completion.d/cam

%files
%defattr(0755,root,root,-)
%{_bindir}/cam
/etc/bash_completion.d/cam

%changelog
