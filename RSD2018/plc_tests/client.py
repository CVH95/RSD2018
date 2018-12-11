import api
import socket

# PLC
_ip = 'localhost'
_port = 5000

# Define global variables
cell_id = 3
events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}
api.global_score = 0

# Create a TCP/IP socket client connected to PLC's server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (_ip, _port)
sock.connect(server_address)

while True:
    _plc = [2,1,0]
    print (" #### CONNECTED TO PLC SERVER #### \n \n \n")
    print ("Connecting to PLC Server in http://" + _ip + ":" + str(_port) + "/")
    api.plc_control(sock, _plc, events_dict)
    print ("Order was completed succesfully. ")
    print ("Total orders completed: " + str(api.global_score))
    print ("Rebboting the cycle...")
    print ("\n \n \n")

