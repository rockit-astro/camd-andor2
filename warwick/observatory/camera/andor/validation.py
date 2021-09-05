#
# This file is part of camd.
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

"""Validation schema used by opsd to verify observation schedule blocks"""

# pylint: disable=unused-argument
def configure_validation_schema(camera):
    """Returns a jsonschema object for validating the
       params object passed to the configure method

       camera takes the camera id (e.g. blue, red) to parse
    """
    if camera == 'red':
        ccd_width_with_overscan = 2088
    else:
        ccd_width_with_overscan = 2048

    return {
        'type': 'object',
        'additionalProperties': False,
        'required': ['exposure'],
        'properties': {
            'temperature': {
                'type': 'number',
                'minimum': -80,
                'maximum': 0,
            },
            'cooler': {
                'type': 'boolean'
            },
            'shutter': {
                'type': 'boolean'
            },
            'gainindex': {
                'type': 'integer',
                'minimum': 0,
                'maximum': 2
            },
            'readoutindex': {
                'type': 'integer',
                'minimum': 0,
                'maximum': 2
            },
            'exposure': {
                'type': 'number',
                'minimum': 0
            },
            'delay': {
                'type': 'number',
                'minimum': 0
            },
            'window': {
                'type': 'array',
                'minItems': 6,
                'maxItems': 6,
                'items': [
                    {
                        'type': 'integer',
                        'minimum': 1
                    },
                    {
                        'type': 'integer',
                        'minimum': 1
                    },
                    {
                        'type': 'integer',
                        'minimum': 1,
                        'maximum': ccd_width_with_overscan
                    },
                    {
                        'type': 'integer',
                        'minimum': 1,
                        'maximum': 2048
                    },
                    {
                        'type': 'integer',
                        'minimum': 1,
                        'maximum': ccd_width_with_overscan
                    },
                    {
                        'type': 'integer',
                        'minimum': 1,
                        'maximum': 2048
                    }
                ]
            }
        }
    }
