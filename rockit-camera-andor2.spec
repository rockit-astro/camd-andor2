Name:      rockit-camera-andor2
Version:   %{_version}
Release:   1
Summary:   Control code for Andor CCD cameras
Url:       https://github.com/rockit-astro/camd-andor2
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/camd
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/andor2_camd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/andor2_camd@.service %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/blue.json %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/red.json %{buildroot}%{_sysconfdir}/camd

%package server
Summary:  Andor CCD camera server
Group:    Unspecified
Requires: python3-rockit-camera-andor2 libusb
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/andor2_camd
%defattr(0644,root,root,-)
%{_unitdir}/andor2_camd@.service

%package data-onemetre
Summary: Andor camera data for the W1m telescope
Group:   Unspecified
%description data-onemetre

%files data-onemetre
%defattr(0644,root,root,-)
%{_sysconfdir}/camd/blue.json
%{_sysconfdir}/camd/red.json

%changelog
