Name:      onemetre-andor-camera-data
Version:   20210910
Release:   0
Url:       https://github.com/warwick-one-metre/camd
Summary:   Camera configuration for Warwick One Metre telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

%description

%build
mkdir -p %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/blue.json %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/red.json %{buildroot}%{_sysconfdir}/camd

%files
%defattr(0644,root,root,-)
%{_sysconfdir}/camd/blue.json
%{_sysconfdir}/camd/red.json

%changelog
