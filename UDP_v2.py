import socket
import cantools
import unittest
import sys

# Rules:
# UDP data field should be >= 8 bytes (cantools library requirement, but offcourse we can manually avoid this rule)

# how to get extended or not +
# how to calc dlc 0-8 variable +
# как выделять поле дата если суммарно разная длина data +
# как понять что начался новый фрейм


# UDP unit parameters:
remote_ip='127.0.0.1' # UDP ip
remote_port='57175' # UPD port

# Socket initialisation
UDP_IP = "127.0.0.1" # current machine address
UDP_PORT = 54915 # current port number
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
rec_msg, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

# UDP frame separation 
data_int=int.from_bytes(rec_msg, 'big')
print(f'frame int: {data_int}')
data_bin=bin(int.from_bytes(rec_msg, 'big'))[2:]
print(f'frame binary: {data_bin}')

# Getting CANframe main parameters

# ID 11 bit
bit_11_id=data_bin[-2:-13:-1][::-1]
print(f'11 bit id: {bit_11_id}')
print(f'11 bit id int: {int(bit_11_id,2)}')

# IDE
IDE=data_bin[-14]
print(f'IDE: {IDE}')


# Standart CAN frame unpacking: DLC, data
if IDE=='0':
    print('Standart CAN frame')
    DLC=data_bin[-16:-20:-1][::-1]
    print(f'DLC: {DLC}')
    DLC_int=int(DLC,2)
    print(f'DLC_int: {DLC_int}')
    id_full=int(bit_11_id,2)
    print(f'full id hex: {id_full}')
    if DLC_int=='0':
        print('DLC = 0, error')        
    elif DLC_int==1:
        data=data_bin[-20:-27:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==2:
        data=data_bin[-20:-35:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==3:
        data=data_bin[-20:-43:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==4:
        data=data_bin[-20:-51:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==5:
        data=data_bin[-20:-59:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==6:
        data=data_bin[-20:-67:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==7:
        data=data_bin[-20:-75:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==8:
        data=data_bin[-20:-83:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_len=len(data)
        print(f'data length: {data_len}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')

# Extended CAN frame unpacking: DLC, data, 18bit id
if IDE=='1':
    print('Extended CAN frame')
    bit_18_id=data_bin[-15:-33:-1][::-1]
    print(f'18 bit id: {bit_18_id}')
    print(f'bit_18_id_int: {int(bit_18_id,2)}')
    
    print(f'18 bit hex: {hex(int(bit_18_id,2))}')
    print(f'11 bit hex: {hex(int(bit_11_id,2))}')
    id_full=int(bit_18_id+bit_11_id,2)
    id_full_hex=hex(id_full)
    print(f'full id hex: {id_full_hex}')
    print(type(id_full))
    
    DLC=data_bin[-36:-40:-1][::-1]
    print(f'DLC: {DLC}')
    DLC_int=int(DLC,2)
    print(f'DLC_int: {DLC_int}')
    if DLC_int=='0':
        print('DLC = 0, error')         
    elif DLC_int==1:
        data=data_bin[-40:-48:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==2:
        data=data_bin[-40:-55:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==3:
        data=data_bin[-40:-62:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==4:
        data=data_bin[-40:-69:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==5:
        data=data_bin[-40:-75:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==6:
        data=data_bin[-40:-82:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==7:
        data=data_bin[-40:-89:-1][::-1]
        print(f'data: {data}')
        print(int(f'data_int:{data}',2))
    elif DLC_int==8:
        data=data_bin[-40:-96:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_len=len(data)
        print(f'data length: {data_len}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')


# Initialisasion DB and decoding parameters
db = cantools.database.load_file('test.dbc', database_format='dbc', encoding='utf-8')
msg_id_rx=str(remote_ip).replace('.','') # getting id for CANdb assotiation
decode=db.decode_message(id_full, data_bytes)
EVSE_present_Current=(decode['EVSE_present_Current'])
EVSE_present_Voltage=(decode['EVSE_present_Voltage'])
print(decode)


# Transmitting CAN in UDP
# # msg_id_tx=648
# # byte_message=db.encode_message(msg_id_tx, {'Maximum_current_cap': Maximum_current_cap, 'Maximum_voltage_cap': Maximum_voltage_cap})
# # sock.sendto(byte_message, (remote_ip, int(remote_port)))


# tests
# # class TestUM(unittest.TestCase):
    # # def setUp(self):
        # # pass

    # # def tearDown(self):
        # # pass

    # # def current_test(self):
        # # self.assertLessEqual(EVSE_present_Current, Maximum_current_cap)

    # # def voltage_test(self):
        # # self.assertLessEqual(EVSE_present_Voltage, Maximum_voltage_cap)

# # if __name__ == '__main__':
    # # unittest.main()