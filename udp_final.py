import string 
import random
import struct
import pprint
import time
from pdcp import receive_PDCP_PDU

print('Enter payload size:')
pack_len = input()
pckt_len=int(pack_len)
print('Enter Packet(Bytes) per sec')
pckt_rate=input()
throughput=int(pckt_rate)

ip_header  = "0x45000020"  # Version, IHL, Type of Service | Total Length
ip_header += "abcd0000"  # Identification | Flags, Fragment Offset
ip_header += "4011a6ec"  # TTL, Protocol | Header Checksum
ip_header += "7f000001"  # Source Address
ip_header += "7f000001"  # Destination Address

udp_header  = "1f401f40" # Source Port | Destination Port
udp_header += "ffff0000" # length | check_sum

data_end="0000" #Type
data_end+="0000"

N=pckt_len*2
time_exe=throughput//pckt_len
# packet_header= ip_header+udp_header

def udp_downlink(data_str):
    payload_end=data_str[58:]
    payload=payload_end[:-8]
    print("Payload: ")
    print(''.join([chr(int(''.join(c), 16)) for c in zip(payload[0::2],payload[1::2])]))


while 1:
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    data=str(res)
    # data="Siddharth"
    data_str=data.encode()
    data_hex=data_str.hex()
    packet=ip_header+udp_header+data_hex+data_end
    # test=packet.decode()
    print(packet)
    receive_PDCP_PDU(packet)
    # udp_downlink(packet)
    time.sleep(time_exe)




