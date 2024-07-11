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

"""client command input handlers"""

import Pyro4
from rockit.common import print
from .config import Config
from .constants import CommandStatus, CameraStatus


def run_client_command(config_path, usage_prefix, args):
    """Prints the message associated with a status code and returns the code"""
    config = Config(config_path)
    commands = {
        'bin': set_binning,
        'delay': set_exposure_delay,
        'exposure': set_exposure,
        'gain': set_gain,
        'readout': set_horizontal_shift_speed,
        'shutter': set_shutter,
        'start': start,
        'status': status,
        'stop': stop,
        'temperature': set_temperature,
        'window': set_window,
        'init': initialize,
        'kill': shutdown
    }

    if len(args) == 0 or (args[0] not in commands and args[0] != 'completion'):
        return print_usage(usage_prefix)

    if args[0] == 'completion':
        if 'gain' in args[-2:]:
            print('high medium low')
        elif 'readout' in args[-2:]:
            print('a b c d')
        elif 'shutter' in args[-2:]:
            print('auto dark')
        elif 'start' in args[-2:]:
            print('continuous')
        elif 'temperature' in args[-2:]:
            print('warm')
        elif len(args) < 3:
            print(' '.join(commands))
        return 0

    try:
        ret = commands[args[0]](config, usage_prefix, args[1:])
    except KeyboardInterrupt:
        # ctrl-c terminates the running command
        ret = stop(config, args)

        # Report successful stop
        if ret == 0:
            ret = -100
    except Pyro4.errors.CommunicationError:
        ret = -101

    # Print message associated with error codes
    if ret not in [-1, 0]:
        print(CommandStatus.message(ret))

    return ret


def status(config, *_):
    """Reports the current camera status"""
    with config.daemon.connect() as camd:
        data = camd.report_status()

    state_desc = CameraStatus.label(data['state'], formatting=True)
    if data['state'] == CameraStatus.Acquiring:
        state_desc += f' ([b]{data["exposure_progress"]:.1f} / {data["exposure_time"]:.1f}s[/b])'
    elif data['state'] == CameraStatus.Waiting:
        state_desc += f' ([b]{data["delay_progress"]:.1f} / {data["delay_total"]:.1f}s[/b])'

    # Camera is disabled
    print(f'   Camera is {state_desc}')
    if data['state'] == CameraStatus.Disabled:
        return 0

    if data['state'] > CameraStatus.Idle:
        if data['sequence_frame_limit'] > 0:
            count = data['sequence_frame_count'] + 1
            limit = data['sequence_frame_limit']
            print(f'   Acquiring frame [b]{count} / {limit}[/b]')
        else:
            print(f'   Acquiring [b]UNTIL STOPPED[/b]')

    temperature_color = 'red'
    if data['temperature_locked']:
        temperature_status = '[b][green]LOCKED[/green][/b]'
        temperature_color = 'green'
    elif not data['cooler_enabled']:
        temperature_status = '[b][red]COOLING DISABLED[/red][/b]'
        temperature_color = 'default'
    else:
        temperature_status = f'[b]LOCKING ON {data["target_temperature"]:.0f}\u00B0C[/b]'

    print(f'   Temperature is [b][{temperature_color}]{data["temperature"]:.0f}\u00B0C[/{temperature_color}][/b] ({temperature_status})')

    shutter_mode = '[green]AUTO[/green]' if data['shutter_enabled'] else '[red]DARK[/red]'
    print(f'   Shutter mode is [b]{shutter_mode}[/b]')
    print(f'   Pre-amp gain is [b]{data["gain_label"]}[/b]')
    print(f'   Readout speed is [b]{data["horizontal_shift_speed_mhz"]:.2f} MHz[/b]')

    wr = data['window_region']
    wb = data['window_bin']
    print(f'   Readout window is [b]\[{wr[0]}:{wr[1]},{wr[2]}:{wr[3]}] px[/b]')
    print(f'   Readout binning is [b]{wb[0]} x {wb[1]} px[/b]')
    print(f'   Exposure time is [b]{data["exposure_time"]:.2f} s[/b]')
    return 0


def set_temperature(config, usage_prefix, args):
    """Set the camera temperature"""
    if len(args) == 1:
        if args[0] == 'warm':
            temp = None
        else:
            temp = int(args[0])
        with config.daemon.connect() as camd:
            return camd.set_target_temperature(temp)
    print(f'usage: {usage_prefix} temperature <degrees>')
    return -1


def set_exposure(config, usage_prefix, args):
    """Set the camera exposure time"""
    if len(args) == 1:
        exposure = float(args[0])
        with config.daemon.connect() as camd:
            return camd.set_exposure(exposure)
    print(f'usage: {usage_prefix} exposure <seconds>')
    return -1


def set_exposure_delay(config, usage_prefix, args):
    """Set the camera pre-exposure delay"""
    if len(args) == 1:
        delay = float(args[0])
        with config.daemon.connect() as camd:
            return camd.set_exposure_delay(delay)
    print(f'usage: {usage_prefix} delay <seconds>')
    return -1


def set_gain(config, usage_prefix, args):
    """Set the camera gain"""
    gains = ['low', 'medium', 'high']
    if len(args) == 1 and args[0] in gains:
        with config.daemon.connect() as camd:
            return camd.set_gain(gains.index(args[0]))
    print(f'usage: {usage_prefix} gain [low|medium|high]')
    return -1


def set_horizontal_shift_speed(config, usage_prefix, args):
    """Set the readout / horizontal shift speed"""
    options = ['a', 'b', 'c', 'd']
    if len(args) == 1 and args[0] in options:
        index = options.index(args[0])
        with config.daemon.connect() as camd:
            return camd.set_horizontal_shift(index)
    print(f'usage: {usage_prefix} readout [a|b|c|d]')
    return -1


def set_shutter(config, usage_prefix, args):
    """Set the camera shutter mode"""
    if len(args) == 1 and (args[0] == 'auto' or args[0] == 'dark'):
        enabled = args[0] == 'auto'
        with config.daemon.connect() as camd:
            return camd.set_shutter(enabled)
    print(f'usage: {usage_prefix} shutter [auto|dark]')
    return -1


def set_binning(config, usage_prefix, args):
    """Set the camera binning"""
    if len(args) == 1:
        # Assume square pixels
        binning = int(args[0])
        with config.daemon.connect() as camd:
            return camd.set_binning(binning, binning)
    print(f'usage: {usage_prefix} bin <pixel size>')
    return -1


def set_window(config, usage_prefix, args):
    """Set the camera readout window"""
    window = None
    if len(args) == 4:
        window = [
            int(args[0]),
            int(args[1]),
            int(args[2]),
            int(args[3])
        ]

    if window or (len(args) == 1 and args[0] == 'default'):
        with config.daemon.connect() as camd:
            return camd.set_window(window)

    print(f'usage: {usage_prefix} window (<x1> <x2> <y1> <y2>|default)')
    return -1


def start(config, usage_prefix, args):
    """Starts an exposure sequence"""
    if len(args) == 1:
        try:
            count = 0 if args[0] == 'continuous' else int(args[0])
        except Exception:
            print('error: invalid exposure count:', args[0])
            return -1

        if args[0] == 'continuous' or count > 0:
            with config.daemon.connect() as camd:
                return camd.start_sequence(count)

    print(f'usage: {usage_prefix} start (continuous|<count>)')
    return -1


def stop(config, *_):
    """Stops any active camera exposures"""
    with config.daemon.connect() as camd:
        return camd.stop_sequence()


def initialize(config, *_):
    """Enables the camera driver"""
    # Initialization can take more than 5 sec, so bump timeout to 20 seconds.
    with config.daemon.connect(20) as camd:
        return camd.initialize()


def shutdown(config, *_):
    """Disables the camera drivers"""
    with config.daemon.connect() as camd:
        return camd.shutdown()


def print_usage(usage_prefix):
    """Prints the utility help"""
    print(f'usage: {usage_prefix} <command> [<args>]')
    print()
    print('general commands:')
    print('   status       print a human-readable summary of the camera status')
    print('   exposure     set exposure time in seconds')
    print('   delay        set pre-exposure delay in seconds')
    print('   shutter      set shutter mode')
    print('   gain         set gain mode')
    print('   readout      set readout speed')
    print('   bin          set readout binning')
    print('   window       set readout window')
    print('   start        start an exposure sequence')
    print()
    print('engineering commands:')
    print('   init         initialize the camera driver')
    print('   temperature  set target temperature and enable cooling')
    print('   kill         disconnect from camera driver')
    print()

    return 0
