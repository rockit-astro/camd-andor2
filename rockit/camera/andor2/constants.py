#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by camd"""

# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

from rockit.common import TFmt


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
        return f'error: Unknown error code {error_code}'


class CameraStatus:
    """Status of the camera hardware"""
    # Note that the Reading status is assumed at status-query time
    # and is never assigned to CameraDaemon._status
    Disabled, Initializing, Idle, Waiting, Acquiring, Reading, Aborting = range(7)

    _labels = {
        0: 'OFFLINE',
        1: 'INITIALIZING',
        2: 'IDLE',
        3: 'WAITING',
        4: 'EXPOSING',
        5: 'READING',
        6: 'ABORTING'
    }

    _formats = {
        0: TFmt.Red,
        1: TFmt.Red,
        2: '',
        3: TFmt.Yellow,
        4: TFmt.Green,
        5: TFmt.Yellow,
        6: TFmt.Red
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._labels:
                return TFmt.Bold + cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN STATUS' + TFmt.Clear

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN STATUS'
