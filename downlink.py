# !/usr/bin/python3

"""
      Description       Bytes
    -----------------------------
    SOF:                0-3
    Control:            4
    Data Length:        5
    MPix Temp:          6-9
    RPI Temp:           10-13
    Frame Counts:       14-17
    Frame Dose Rate:    18-21
    Frame Count ID:     22-25
    Device ID:          26-29
    Unix Timestamp:     30-33
    Error Flags:        34-35
    Checksum:           36-39
    EOF:                40
"""

import struct


def float_to_hex(value):
    hex_string = hex(struct.unpack('<I', struct.pack('<f', value))[0]).replace('0x','')
    return bytes.fromhex(hex_string)


def int_to_hex(value):
    hex_string = format(value, '#010x').replace('0x', '')
    return bytes.fromhex(hex_string)

def downlink_packet(ser, data, error=None):
    """
    :param ser: Take a serial port
    :param data: Take a dictionary of updated values
    :return: void

    Mutate the data packet template using a dictionary
    of key, value pairs into thier respective binary strings
    then send each string down the serial port
    """

    packet = dict(SOF=b'@\xA333',
                  CTRL=b'\x0B',
                  DATALEN=b'\xDD',
                  MPTMP=b'\xCC\xCC\xCC\xCC',
                  RPiTMP=b'\xCC\xCC\xCC\xCC',
                  FrCOUNTS=b'\xDD\xDD\xDD\xDD',
                  FrDRATE=b'\xEE\xEE\xEE\xEE',
                  FrCountID=b'\xFF\xFF\xFF\xFF',
                  DID=b'\x11\x11\x11\x11',
                  TIME=b'\x10\x11\x10\x11',
                  ERR=b'\xEE\xEE',
                  CHKSUM=b'\xCC\xEE\xCC\xEE',
                  EOF=b'\x0F')

    packet['MPTMP'] = float_to_hex(data['MPTMP'])
    packet['RPiTMP'] = float_to_hex(data['RPiTMP'])
    packet['FrCOUNTS'] = int_to_hex(data['FrCOUNTS'])
    packet['FrDRATE'] = float_to_hex(data['FrDRATE'])
    packet['FrCountID'] = int_to_hex(data['FrCountID'])
    packet['DID'] = int_to_hex(data['DID'])
    packet['TIME'] = int_to_hex(data['TIME'])

    for key, value in packet.items():
        ser.write(value)

