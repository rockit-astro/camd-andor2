## Andor camera daemon

`andor_camd` interfaces with and wraps Andor USB CCD cameras and exposes them via Pyro.

`cam` is a commandline utility for controlling the cameras.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the observatory software architecture and instructions for developing and deploying the code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/camd`.
A configuration file is specified when launching the camera server, and the `cam` frontend will search for files matching the specified camera id when launched.

The configuration options are:
```python
{
  "daemon": "onemetre_blue_camera", # Run the camera server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "pipeline_daemon": "onemetre_pipeline", # The daemon that should be notified to hand over newly saved frames for processing.
  "pipeline_handover_timeout": 10, # The maximum amount of time to wait for the pipeline daemon to accept a newly saved frame. The exposure sequence is aborted if this is exceeded.
  "log_name": "andor_camd@blue", # The name to use when writing messages to the observatory log.
  "control_machines": ["OneMetreDome", "OneMetreTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `warwick.observatory.common.IP`.
  "camera_serial": 11575, # Camera serial number. If not known, set a dummy value and look at the list reported when the daemon scans for cameras.
  "temperature_setpoint": -30, # Default CCD temperature in celsius.
  "temperature_query_delay": 1, # Amount of time in seconds to wait between querying the camera temperature and cooling status.
  "gain_index": 0, # Default gain setting.
  "horizontal_shift_index": 2, # Default readout speed.
  "overscan": [0, 0], # Number of columns to trim from the left and right of the image.
  "filter": "BG40", # Value to use for the FILTER fits header keyword.
  "camera_id": "BLUE", # Value to use for the CAMERA fits header keyword.
  "output_path": "/var/tmp/", # Path to save temporary output frames before they are handed to the pipeline daemon. This should match the pipeline incoming_data_path setting.
  "output_prefix": "blue", # Filename prefix to use for temporary output frames.
  "expcount_path": "/var/tmp/blue-counter.json" # Path to the json file that is used to track the continuous frame and shutter numbers.
}
```

### Initial Installation

The Andor SDK is required for `observatory-andor-camera-server`, and must be installed separately.
Download the latest SDK version from the [Docs repository](https://github.com/warwick-one-metre/docs/tree/master/andor/sdk), extract it, and then install using:
```
sudo ./install_andor
```
Select option 5 (All USB Cameras).

Under CentOS 8 the `libusb-devel` package required for the andor library to find cameras (note: `libusbx-devel` doesn't work) is available through the PowerTools repository
```
sudo yum config-manager --set-enabled PowerTools
```

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package           | Description |
| ----------------- | ------ |
| onemetre-andor-camera-data  | Contains the json configuration files for the Warwick One Metre dual-camera instrument. |
| observatory-andor-camera-server | Contains the `andor_camd` server and systemd service files for the camera server. |
| observatory-andor-camera-client | Contains the `cam` commandline utility for controlling the camera server. |
| python3-warwick-andor-camera | Contains the python module with shared code. |

The `observatory-andor-camera-server observatory-andor-camera-client onemetre-andor-camera-data` packages should be installed on the `onemetre-tcs` machine, then the systemd service should be enabled:
```
sudo systemctl enable andor_camd@<config>
sudo systemctl start andor_camd@<config>
```

where `config` is `blue` then `red` for the two cameras.

Now open a port in the firewall so the TCS and dashboard machines can communicate with the camera server:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```

where `port` is the port defined in `warwick.observatory.common.daemons` for the daemon specified in the camera config.

The `observatory-andor-camera-client` and `onemetre-andor-camera-config` can be installed on both the TCS and dome machines for centralized control.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl stop andor_camd@<config>
sudo systemctl start andor_camd@<config>
```

### Testing Locally

The camera server and client can be run directly from a git clone:
```
./andor_camd test.json
CAMD_CONFIG_ROOT=. ./cam blue status
```
