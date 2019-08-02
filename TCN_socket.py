import socket
import time
import sys
import pickle
import traceback
#import struct
#from multiprocessing.connection import Listener, Client


class UDP_server(object):
    ''' Class for socket server '''

    def __init__(self, port = 50000, setblocking = 0,ip = '127.0.0.1'):
        self.port = port
        self.ip = ip
        self.setblocking = setblocking

        # Send list method ( 'socket' or 'multi')
        self.method = 'socket'

        # Create UDP server
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setblocking(self.setblocking)
            self.sock.bind((self.ip, self.port))
            print('Server initiate - '+ self.ip+ ' : '+ str(self.port))

        except Exception as e:
            self.sock.close()
            print('Cancel bind process \n\n')
            print(e)

    def recv_string(self, length = 11):
        try:
            receive_str = self.sock.recv(length).decode('utf-8')
            return receive_str
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.sock.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        except socket.error as e:
            #print(e)
            pass
        except Exception as e:
            print(e)
            self.sock.close()

    def recv_list(self, length = 4096):
        try:
            receive_list_flag = True
            receive_list = []
            while receive_list_flag:
                try:
                    temp_receive_list = self.connection[0].recv(length)
                    receive_list.append(temp_receive_list)
                    if sys.getsizeof(temp_receive_list) < length:
                        receive_list_flag = False
                except:
                    receive_list_flag = False
            if receive_list != [b'']:
                receive_list = pickle.loads(b"".join(receive_list)) 
                return receive_list
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error:
        #     #print(e)
        #     pass
        except:
            traceback.print_exc()
            self.close()
            raise KeyboardInterrupt

            

    def send_string(self, message = '', port=50000, ip = '127.0.0.1'):
        ''' Send string to target port (default IP is 127.0.0.1)'''

        try:
            if port != self.port or ip != self.ip:
                self.sock.sendto(message.encode('utf-8') ,(self.ip ,self.port) ) # Send message ( I forgot what's the return value of sendto() )
            else:
                self.sock.sendto(message.encode('utf-8') , (ip,port) )
        except:
            self.sock.close()
            traceback.print_exc()

    def send_list(self, list = [], port=50000, ip = '127.0.0.1'):
        '''send list to target port (default IP is 127.0.0.1)'''
        try:
            if port != self.port or ip != self.ip:
                self.sock.sendto(pickle.dumps(list) , (ip,port) )
            else:
                self.sock.sendto(pickle.dumps(list) , (self.ip, self.port) )
                
        except:
            self.sock.close()
            traceback.print_exc()

    def close(self):
        ''' Close server '''
        self.sock.close()
        # print('Server close without error')


class UDP_client(object):
    ''' Class for UDP_client '''
    def __init__(self, port = 50000,setblocking = 0, ip='127.0.0.1'):
        self.port = port
        self.ip = ip
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setblocking(setblocking)
        except:
            self.sock.close()
            traceback.print_exc()
            print('\nsocket client fail initialize')
    
    def recv_string(self, length = 11):
        try:
            receive_str = self.sock.recv(length).decode('utf-8')
            return receive_str
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.sock.close() # Unbind socket from the adress
            sys.exit(-0) # Exit program
        except socket.error:
            pass
        except:
            self.sock.close()
            traceback.print_exc()

    def recv_list(self, length = 4096):
        try:
            receive_list_flag = True
            receive_list = []
            while receive_list_flag:
                try:
                    temp_receive_list = self.connection[0].recv(length)
                    receive_list.append(temp_receive_list)
                    if sys.getsizeof(temp_receive_list) < length:
                        receive_list_flag = False
                except:
                    receive_list_flag = False
            if receive_list != [b'']:
                receive_list = pickle.loads(b"".join(receive_list)) 
                return receive_list
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error:
        #     #print(e)
        #     pass
        except:
            traceback.print_exc()
            self.close()
            raise KeyboardInterrupt

    def send_string(self, message = '', port=50000, ip = '127.0.0.1'):
        ''' Send string to target port (default IP is 127.0.0.1)'''
        try:
            if port != self.port or ip != self.ip:
                self.sock.sendto(message.encode('utf-8') ,(self.ip ,self.port) ) # Send message ( I forgot what's the return value of sendto() )
            else:
                self.sock.sendto(message.encode('utf-8') , (ip,port) )
        except:
            self.sock.close()
            traceback.print_exc()

    def send_list(self, list = [], port=50000, ip = '127.0.0.1'):
        '''send list to target port (default IP is 127.0.0.1)'''
        try:
            self.sock.sendto(pickle.dumps(list) , (ip,port) )
        except Exception as e:
            self.sock.close()
            print(e)

    def close(self):
        ''' Close server '''
        self.sock.close()
        # print('Client close without error')

    
#######################################################################
#######################################################################
#        ______________       ____________         ___________        #
#              |             |                     |         |        #
#              |             |                     |         |        #
#              |             |                     |_________|        #
#              |             |                     |                  #        
#              |             |                     |                  #
#              |             |____________         |                  #
#                                                                     #
#######################################################################
#######################################################################

class TCP_server(object):
    ''' Class for socket server '''

    def __init__(self, port = 50000, setblocking = 1,ip = '127.0.0.1'):
        self.port = port
        self.ip = ip
        self.setblocking = setblocking
        self.connection = None

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(self.setblocking)
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
            self.connection = self.sock.accept()
            self.sock.close()
            self.server_connection_file_descriptor = self.connection[0].fileno()
            # print('Client connected')

        except:
            self.close()
            print('Cancel bind process \n\n')
            traceback.print_exc()



    def blocking(self, setblocking=True):
        self.sock.setblocking(setblocking)
        


    def recv_string(self, length = 1):
        try:
            receive_str = self.connection[0].recv(length)
            if receive_str != None:
                receive_str = receive_str.decode('utf-8')
                return receive_str
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error:
        #     #print(e)
        #     pass
        except:
            traceback.print_exc()
            self.close()
            raise KeyboardInterrupt



    def recv_list(self, length = 4096):
        try:
            receive_list_flag = True
            receive_list = []
            while receive_list_flag:
                try:
                    temp_receive_list = self.connection[0].recv(length)
                    receive_list.append(temp_receive_list)
                    if sys.getsizeof(temp_receive_list) < length:
                        receive_list_flag = False
                except:
                    receive_list_flag = False
            if receive_list != [b'']:
                receive_list = pickle.loads(b"".join(receive_list)) 
                return receive_list
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error:
        #     #print(e)
        #     pass
        except:
            traceback.print_exc()
            self.close()
            raise KeyboardInterrupt



    def send_string(self, message = ''):
        ''' Send string to target client'''
        try:
            self.connection[0].sendall(message.encode('utf-8') ) # Send message ( I forgot what's the return value of sendto() )
        except:
            self.close()
            traceback.print_exc()

    def send_list(self, list = []):
        '''send list to target port (default IP is 127.0.0.1)'''
        try:
            self.connection[0].sendall(pickle.dumps(list))
        except:
            self.close()
            traceback.print_exc()

    def close(self):
        ''' Close server '''
        self.sock.close()
        if self.connection != None:
            self.connection[0].close()




class TCP_client(object):
    ''' Class for UDP_client '''
    def __init__(self, port = 50000, ip='127.0.0.1'):
        self.port = port
        self.ip = ip
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip,self.port))
        except:
            self.sock.close()
            traceback.print_exc()
            print('socket client fail initialize')
    
    def recv_string(self, length = 11):
        try:
            
            receive_str = self.sock.recv(length).decode('utf-8')
            return receive_str
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.sock.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error as e:
        #     print(e)
        #     pass
        except:
            traceback.print_exc()
            self.sock.close()

    def recv_list(self, length = 4096):
        try:
            receive_list_flag = True
            receive_list = []
            while receive_list_flag:
                try:
                    temp_receive_list = self.sock.recv(length)
                    receive_list.append(temp_receive_list)
                    if sys.getsizeof(temp_receive_list) < length:
                        receive_list_flag = False
                except:
                    receive_list_flag = False
            if receive_list != [b'']:
                receive_list = pickle.loads(b"".join(receive_list)) 
                return receive_list
        
        except socket.timeout: # if server didn't get any data in a period of time 
            pass               # Do nothing and pass  , the return data is 'None' 
        except KeyboardInterrupt: 
            self.close() # Unbind socket from the adress
            sys.exit(0) # Exit program
        # except socket.error as e:
        #     print(e)
        #     pass
        except:
            traceback.print_exc()
            self.close()
            raise KeyboardInterrupt



    def send_string(self, message = '', port=50000, ip = '127.0.0.1'):
        ''' Send string to target port (default IP is 127.0.0.1)'''
        try:
            if port != self.port or ip != self.ip:
                self.sock.sendto(message.encode('utf-8') , (self.ip ,self.port)  ) # Send message ( I forgot what's the return value of sendto() )
            else:
                self.sock.sendto(message.encode('utf-8') , (ip,port))
        except:
            self.close()
            traceback.print_exc()
            raise KeyboardInterrupt



    def send_list(self, list = [], port=50000, ip = '127.0.0.1'):
        '''send list to target port (default IP is 127.0.0.1)'''
        try:
            if port != self.port or ip != self.ip:
                self.sock.sendto(pickle.dumps(list) , (self.ip, self.port) )
            else:
                self.sock.sendto(pickle.dumps(list) , (ip,port) )
        except:
            self.close()
            traceback.print_exc()
            raise KeyboardInterrupt

    def close(self):
        ''' Close server '''
        self.sock.close()
        # print('Client close without error')



