Name:      onemetre-{CAMERA}-camera-client
Version:   1.0
Release:   0
Url:       https://github.com/warwick-one-metre/camd
Summary:   Camera control client for the Warwick one-metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-pyds9

%description
Part of the observatory software for the Warwick one-meter telescope.

{CAMERA} is a commandline utility for controlling the {CAMERA} camera.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/{CAMERA} %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/{CAMERA} %{buildroot}/etc/bash_completion.d/{CAMERA}

%files
%defattr(0755,root,root,-)
%{_bindir}/{CAMERA}
/etc/bash_completion.d/{CAMERA}

%changelog
