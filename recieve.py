import socket
import struct
import cantools

# Standart CAN frame: 06 40 03 24 0a 02

# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    print(type(can_id))
    print(type(can_dlc))
    print(type(data))
    return (can_id, can_dlc, data[:can_dlc])

# create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(("vcan0",))



while True:
    cf, addr = s.recvfrom(16)
    print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))

    db = cantools.database.load_file('test.dbc', database_format='dbc', encoding='utf-8')
    data_field=dissect_can_frame(cf)[2][::-1]
    id_can=dissect_can_frame(cf)[0]
    decode=db.decode_message(id_can, data_field)
    EVSE_present_Current=(decode['EVSE_present_Current'])
    EVSE_present_Voltage=(decode['EVSE_present_Voltage'])
    print(decode)
