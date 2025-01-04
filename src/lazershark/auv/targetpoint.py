"""
targetpoint.py

Copyright (C) 2024-2025 Cabrillo Robotics Club

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Cabrillo Robotics Club
6500 Soquel Drive Aptos, CA 95003
cabrillorobotics@gmail.com
"""
from sys import stderr
from serial import Serial
from binascii import crc_hqx
from struct import unpack

class FailedCRC(Exception):
    pass


class MismatchedFrameID(Exception):
    pass

def get_bytes(n: int, length: int) -> bytes:
    """
    Int to bytes (big endian) wrapper.

    Args:
        n: Integer to convert into bytes.
        length: Length of bytes object to use.

    Returns:
        Bytes in big endian representing integer `n`.
    """
    return n.to_bytes(length, byteorder="big")

# Table 7-2: TPTCM Command Set
# Map command name to command frame ID
_cmd_frame_id = {
    "kGetModInfo":          get_bytes(0x01, 1),  # Queries the device’s type and firmware revision.
    "kSetDataComponents":   get_bytes(0x03, 1),  # Sets the data components to be output.
    "kGetData":             get_bytes(0x04, 1),  # Queries the TPTCM for data
}

# Table 7-6: Component Identifiers
# Map component name to component IDs
_data_comp = {
    "kHeading":         0x05,
    "kPitch":           0x18,
    "kRoll":            0x19,
    "kHeadingStatus":   0x4F,
    "kQuaternion":      0x4D,
    "kTemperature":     0x07,
    "kDistortion":      0x08,
    "kCalStatus":       0x09,
    "kAccelX":          0x15,
    "kAccelY":          0x16,
    "kAccelZ":          0x17,
    "kMagX":            0x1B,
    "kMagY":            0x1C,
    "kMagZ":            0x1D,
    "kGyroX":           0x4A,
    "kGyroY":           0x4B,
    "kGyroZ":           0x4C,
}

# Table 7-6: Component Identifiers
# Map component ID to number of bytes, struct format character in big endian*, and component name
# *https://docs.python.org/3/library/struct.html#format-characters
_comp_fmt = {
    0x05: (4,  ">f", "kHeading"),
    0x18: (4,  ">f", "kPitch"),
    0x19: (4,  ">f", "kRoll"),
    0x4F: (1,  ">B", "kHeadingStatus"),
    0x4D: (16, ">f", "kQuaternion"),  # Quaternions have four floats, handle separately
    0x07: (4,  ">f", "kTemperature"),
    0x08: (1,  ">?", "kDistortion"),
    0x09: (1,  ">?", "kCalStatus"),
    0x15: (4,  ">f", "kAccelX"),
    0x16: (4,  ">f", "kAccelY"),
    0x17: (4,  ">f", "kAccelZ"),
    0x1B: (4,  ">f", "kMagX"),
    0x1C: (4,  ">f", "kMagY"),
    0x1D: (4,  ">f", "kMagZ"),
    0x4A: (4,  ">f", "kGyroX"),
    0x4B: (4,  ">f", "kGyroY"),
    0x4C: (4,  ">f", "kGyroZ"),
}

class TargetPoint:
    def __init__(self, port: int, baud_rate: int = 38400) -> None:
        """
        Initialize a `TargetPoint` object.

        Args:
            port: The `/dev/ttyUSB` port number to communicate over.
            baud_rate: The baud rate for the serial connection. Defaults to 38400.
        """
        # Initialize serial port
        self._serial = Serial(f"/dev/ttyUSB{port}", baud_rate)
        print(f"Port /dev/ttyUSB{port} open: {self._serial.is_open}", file=stderr)
        # Queries the device's type and firmware revision number
        self._serial.write(TargetPoint._create_cmd(_cmd_frame_id["kGetModInfo"]))
        print(f"kGetModInfoResp: {TargetPoint._fmt_response_debug(self._read_response())}", file=stderr)
        self._data = {}

    def select_comp(self, *args: str) -> None:
        """
        Select components to retrieve from the TPTCM when `read_data()` is called.

        See TargetPoint TCM User Manual (Ver 1.6), Table 7-6: Component Identifiers.

        Args:
            args: String(s) matching the components in Table 7-6 describing data to request.
        """
        # Create payload to request specified components
        payload = bytearray(_cmd_frame_id["kSetDataComponents"])
        payload.append(len(args))
        for arg in args:
            payload.append(_data_comp[arg])
            self._data[arg] = None
        # Generate and send command
        cmd = TargetPoint._create_cmd(payload)
        self._serial.write(cmd)
