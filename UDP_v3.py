import socket
import cantools
import unittest
import sys
import struct

# Hints:
# Extended hex for "packet sender": 14080006802
# Standart hex for "packet sender": 18240A02

# "Packet sender" were using for transmiting CAN Frame in UDP format

# Задание:
'''
Компьютер с установленной ОС Linux подключен к локальной сети. 
На нём настроен виртуальный CAN-интерфейс vcan. В сети есть устройство,
физически подключенное к CAN-шине, которое преобразует все принятые CAN-сообщения в UDP и
 отправляет их на вышеуказанный компьютер. В свою очередь, это устройство слушает определенный UDP-порт,
а принятые с него данные отправляет в интерфейс CAN. Адресация в сети и номера портов статичны и известны.
Протокол упаковки UDP в CAN вам предстоит придумать при выполнении задания, при этом особых требований к протоколу не выдвигается.

Реализуйте приложение на языке Python3 для данной Linux-машины, которое позволит виртуальным vcan обмениваться между собой CAN-сообщениями 
(например, с помощью can-utils) и данными с физической CAN-шиной на удалённом устройстве.
Будет плюсом, если вы покроете приложение юнит-тестами для 1-2 вариантов его использования.
Пожалуйста, укажите ссылку на файл с выполненным тестовым заданием.
'''




# UDP unit parameters:
remote_ip='127.0.0.1' # UDP ip
remote_port=input('enter port: ') # UPD port

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
    print(f'full id int: {id_full}')
    if DLC_int==1:
        data=data_bin[-20:-27:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==2:
        data=data_bin[-20:-35:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==3:
        data=data_bin[-20:-43:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==4:
        data=data_bin[-20:-51:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==5:
        data=data_bin[-20:-59:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==6:
        data=data_bin[-20:-67:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==7:
        data=data_bin[-20:-75:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
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
    if DLC_int==1:
        data=data_bin[-40:-48:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==2:
        data=data_bin[-40:-55:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==3:
        data=data_bin[-40:-62:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==4:
        data=data_bin[-40:-69:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==5:
        data=data_bin[-40:-75:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==6:
        data=data_bin[-40:-82:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
    elif DLC_int==7:
        data=data_bin[-40:-89:-1][::-1]
        print(f'data: {data}')
        data_int=int(data,2)
        print(f'data_int:{data_int}')
        data_bytes=data_int.to_bytes(8, 'big')
        print(f'data in bytes: {data_bytes}')
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
decode=db.decode_message(id_full, data_bytes)
EVSE_present_Current=(decode['EVSE_present_Current'])
EVSE_present_Voltage=(decode['EVSE_present_Voltage'])
print(decode)


# # Transmitting UDP to vcan0
can_frame_fmt = "=IB3x8s"

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)
    
# create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(("vcan0",))

try:
    s.send(build_can_frame(id_full, data_bytes))
except socket.error:
    print('Error sending CAN frame')



# Recieving CAN from vcan0
def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return (can_id, can_dlc, data[:can_dlc])

cf, addr = s.recvfrom(16)
print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))


# Convert and transmit vcan to UDP
can_id_vcan0=dissect_can_frame(cf)[0]
can_data_vcan0=dissect_can_frame(cf)[2][::-1]
transmit_message=cf
sock.sendto(transmit_message, (remote_ip, int(remote_port)))


# Tests
class TestUDPCAN(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dlc_not_empty(self):
        self.assertGreater(DLC_int,0)
        self.assertLessEqual(DLC_int,8)
        
    def test_IDE_true_false(self):
        self.assertLessEqual(int(IDE,2),1)
        self.assertGreaterEqual(int(IDE,2),0)
        
    def test_SOF_dominant(self):
        SOF=int(data_bin[-1])
        self.assertEqual(SOF,0)
        


if __name__ == '__main__':
    unittest.main()
    
'''
Заключение:
• В задании не указывается в каком виде присылаются данные в UDP прокотоле: полный CAN Frame (SOF, 11bitID, RTR/SRR и т.д) или только поле Data, поэтому
использовались данные 18240A02 hex в Packet sender, в которых содержатся данные от начала CAN Frame (SOF) до (Data) включительно, не учитывается CRC, ACK, EOF и т.д.

• Полученные данные с vcan0 пересылаются в UPD со следующим содержанием: can_id, can_dlc и can_data, так как библиотека vcan не пакует полный CAN frame.
'''