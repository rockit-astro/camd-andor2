Name:      observatory-andor-camera-server
Version:   20220726
Release:   0
Url:       https://github.com/warwick-one-metre/camd
Summary:   Control server for Andor CCD cameras.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3 python3-Pyro4 python3-numpy python3-astropy
Requires:  python3-warwick-observatory-common python3-warwick-observatory-andor-camera
Requires:  observatory-log-client
# Required for the andor SDK to detect the cameras
# Under CentOS 8 this requires the powertools repository to be enabled
Requires: libusb-devel

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

%{__install} %{_sourcedir}/andor_camd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/andor_camd@.service %{buildroot}%{_unitdir}

%files
%defattr(0755,root,root,-)
%{_bindir}/andor_camd
%defattr(-,root,root,-)
%{_unitdir}/andor_camd@.service

%changelog
