import TCN_socket
import time
import traceback
import subprocess
import sys

'''Portocol'''
''' "C" to Main , "L" to LiDAR , "S" to STM32 , "G" to GPIO , "X" to xbox, "V" to Vision , "M" to motion '''

try:
    commander_client = TCN_socket.UDP_client(50000)
    commander_client.send_string('C')

    commander_connection = commander_client.recv_string()
    if commander_connection == 'S':
        stm32_server = TCN_socket.UDP_server(50001,1)
        subprocess.Popen('python TCN_STM32_main.py',shell=True)
        stm32_connection = stm32_server.recv_string()
        print(stm32_connection)
        commander_client.send_string('S')
        

    
    end = commander_client.recv_string()
    print(end)
    if end == 'E':
        commander_client.close()
        stm32_server.send_string('E')
        time.sleep(1)
        stm32_server.close()



    # xbox_server = TCN_socket.UDP_server(50002,1)
    # xbox_connection = xbox_server.recv_string()
    # if xbox_connection == 'X':
    #     commander_client.send_string('X')
        

        

except:
    traceback.print_exc()
    commander_client.close()
    stm32_server.close()

sys.exit()










class bridge_portocol(object):

    def Command_potorcol(self,command):
        if type(command) == str:
            pass

