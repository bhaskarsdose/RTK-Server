from pymavlink import mavutil
import socket
import struct

master = mavutil.mavlink_connection('COM58',baud=115200)
inject_seq_nr = 0
def send_rtcm_msg(data):
        global inject_seq_nr
        msglen = 180;
       
        if (len(data) > msglen * 4):
            print("DGPS: Message too large", len(data))
            return
       
        # How many messages will we send?
        msgs = 0
        if (len(data) % msglen == 0):
            msgs = len(data) / msglen
        else:
            msgs = (len(data) / msglen) + 1
       
        for a in range(0, msgs):
           
            flags = 0
           
            # Set the fragment flag if we're sending more than 1 packet.
            if (msgs) > 1:
                flags = 1
           
            # Set the ID of this fragment
            flags |= (a & 0x3) << 1
           
            # Set an overall sequence number
            flags |= (inject_seq_nr & 0x1f) << 3
           
           
            amount = min(len(data) - a * msglen, msglen)
            datachunk = data[a*msglen : a*msglen + amount]
           
            master.mav.gps_rtcm_data_send(
                flags,
                len(datachunk),
                bytearray(datachunk.ljust(180, '\0')))
       
        # Send a terminal 0-length message if we sent 2 or 3 exactly-full messages.    
        if (msgs < 4) and (len(data) % msglen == 0) and (len(data) > msglen):
            flags = 1 | (msgs & 0x3)  << 1 | (inject_seq_nr & 0x1f) << 3
            master.mav.gps_rtcm_data_send(
                flags,
                0,
                bytearray("".ljust(180, '\0')))

        inject_seq_nr += 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9000))
mreq = struct.pack("=4sl", socket.inet_aton("232.1.1.11"), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
while True:
    data = sock.recv(2200)   
    print(data)
    send_rtcm_msg(data)
