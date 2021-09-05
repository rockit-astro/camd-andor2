#
# This file is part of camd
#
# camd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# camd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with camd.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by camd"""

# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

FMT_GREEN = u'\033[92m'
FMT_RED = u'\033[91m'
FMT_CYAN = u'\033[96m'
FMT_YELLOW = u'\033[93m'
FMT_BOLD = u'\033[1m'
FMT_CLEAR = u'\033[0m'

class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2
    InvalidControlIP = 3

    CameraNotFound = 5

    # Command-specific codes
    CameraNotInitialized = 10
    CameraNotIdle = 11
    CameraNotUninitialized = 14
    CameraNotAcquiring = 15

    TemperatureOutsideLimits = 20
    BinningIncompatibleWithWindow = 30
    WindowIncompatibleWithBinning = 31
    WindowOutsideCCD = 32
    InvalidWindow = 33

    InvalidGainIndex = 40
    InvalidShiftSpeedIndex = 41

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        3: 'error: command not accepted from this IP',
        5: 'error: camera hardware not found',

        # Command-specific codes
        10: 'error: camera has not been initialized',
        11: 'error: camera is not idle',
        14: 'error: camera has already been initialized',
        15: 'error: camera is not acquiring',

        20: 'error: requested temperature is outside the supported limits',

        # Readout geometry
        30: 'error: binning does not evenly divide readout window',
        31: 'error: window size is not compatible with the current binning',
        32: 'error: window extends outside the bounds of the ccd',
        33: 'error: invalid readout window',

        40: 'error: invalid gain',
        41: 'error: invalid shift speed',

        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with camera daemon',
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return 'error: Unknown error code {}'.format(error_code)

class CameraStatus:
    """Status of the camera hardware"""
    # Note that the Reading status is assumed at status-query time
    # and is never assigned to CameraDaemon._status
    Disabled, Initializing, Idle, Waiting, Acquiring, Reading, Aborting = range(7)

    _labels = {
        0: FMT_BOLD + FMT_RED + 'OFFLINE' + FMT_CLEAR,
        1: FMT_BOLD + FMT_RED + 'INITIALIZING' + FMT_CLEAR,
        2: FMT_BOLD + 'IDLE' + FMT_CLEAR,
        3: FMT_BOLD + FMT_YELLOW + 'WAITING' + FMT_CLEAR,
        4: FMT_BOLD + FMT_GREEN + 'EXPOSING' + FMT_CLEAR,
        5: FMT_BOLD + FMT_YELLOW + 'READING' + FMT_CLEAR,
        6: FMT_BOLD + FMT_RED + 'ABORTING' + FMT_CLEAR
    }

    @classmethod
    def label(cls, status):
        """Returns a human readable string describing a status"""
        if status in cls._labels:
            return cls._labels[status]
        return FMT_RED + FMT_BOLD + 'UNKNOWN STATUS' + FMT_CLEAR

class CameraGain:
    """Camera gain levels"""
    High, Medium, Low = range(3)
    _labels = {
        0: FMT_BOLD + 'HIGH' + FMT_CLEAR,
        1: FMT_BOLD + 'MEDIUM' + FMT_CLEAR,
        2: FMT_BOLD + 'LOW' + FMT_CLEAR,
    }

    @classmethod
    def label(cls, status):
        """Returns a human readable string describing a gain"""
        if status in cls._labels:
            return cls._labels[status]
        return FMT_RED + FMT_BOLD + 'UNKNOWN GAIN' + FMT_CLEAR
