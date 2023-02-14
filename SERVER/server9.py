#TODO::

# PACKAGE_PROJECT       [IN_PROGRESS]

#LOGIN/REGISTER         [DONE]:[STD]:
    # {NEXT}->{CROSS_ACCOUNT}
#CONTACT_LIST           [DONE]
#ADD_CONTACT            [DONE]
#CONTACT_STATUS         [DONE]
#MESSAGING              [NEXT]:[DIRECT_SEND if ONLINE]: 
    # {NEXT}->{SAVE_TILL_ONLINE}
#FORMS{DYNAMIC}         []
#MAPS                   []
#CALENDER               []
#CONNECT -> API         []
#SEARCH                 [?]


try:
    import socket
    import string
    import sys
    from threading import Thread, ThreadError
    import threading
    from datetime import datetime


    from BASE_PY import *
    from STACK_PY import *
    from SERVER_PY import *

except Exception as e:
    print("[IPMORT]::[ERROR]:: ", str(e))

class server():
    def __init__(self, **kwargs):
        super(server, self).__init__(**kwargs)

        #IMPORTS
        # BASE
        from BASE_PY.File_Man import File_man
        self.FM         = File_man()

        # SERVER
        from SERVER_PY.contacts import Conts_
        self.CONTS      = Conts_()

        from SERVER_PY.msg_ing import Msgs_
        self.MSG        = Msgs_()

        from SERVER_PY.users import Users_
        self.USER       = Users_()

        # STACK_OPTS
        from STACK_PY.stack_opt import Stack_Opt
        self.SO         = Stack_Opt()

        #CONNECTIONS
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8085
        self.addr = (self.host, self.port)

        #ACTIVE USERS
        self.LOGGED_IN = []


        # THREADS 
        self.threads = []

    #SEND_METHODE
    def reply(self, conn, data):
        try:
            msg_len = len(data)
            send_len = str(msg_len).encode()
            send_len += b' ' * (64 - len(send_len))
            #print(f'[SENDING]:: {send_len}')
            #print(f'[SENDING]:: {data}')
            conn.send(send_len)
            conn.send(data.encode())
            #print("[SENT]: ", str(data))
            return
        except Exception as e:
            print('REPLY_ERROR:: ', str(e))


    #CLIENT_THREAD_HANDLE
    def handle_client(self, conn, addr):
        try:
            connections = True
            self.user = ""
            user = ""
            self.active = False
            get_conts = False
            client = []
            client = [conn, addr]
            print("[Client]:[CONNECTED]:", str(addr))
            data = ""
            self.data = ""
            data_len = 0
            pl = ""
            self.E = threading.Event()
            self.reply(conn, "WELCOME")
        except Exception as e:
            print("[ERROR_SETTING_VARIABLES]: ", str(e))
        while connections == True:
            #print("[CURRENT_USER] :: ", str(self.user))
            #if len(user) > 0:
            #    self.update_User(client, user, "ONLINE")
            #    print(f"[SELF.USER]::{addr}::[ONLINE]::{user}")
            try:
                try:
                    try: # GET IN_BOUND
                        data_len = int(conn.recv(64).decode())
                        if not data_len:
                            #print("WAITING_DATA_LEN:: ")
                            self.E.wait()
                        #print("[DATA_LEN]: ", str(data_len))
                        if data_len > 0:
                            #print("[WAITING]:>:[IN_COMM]")
                            self.data = str(conn.recv(data_len).decode())
                            if not self.data:
                                self.E.wait()                                
                            else:
                                data = self.data
                                #print("[IN_COMM]:self: ", str(self.data))
                                self.data = ''
                                #print("[IN_COMM]:data: ", str(data))
                    except:
                        print(f'[CLIENT_DISCONNECTED]: {addr} ')
                        if user:
                            self.update_User(client, user, "OFFLINE")
                            print(f"[DISCONN]::{addr}::[LOGGED_OFF]::{user}")
                            connections = False
                        return
                        #sys.exit(1)
                    
                    # STACK_OPTS: LEADS
                    if "LEADS" in data:

                        print("[STACK]")
                        #st_data = data.split("*")
                        #for st_ in st_data:
                        #    print(f"[ST_]:[>{str(st_)}<]")
                        self.SO.main(data)

                    # MESSAGING
                    if "MSG_TO" in data:
                        #print("[MSG_TO]:", str(data))
                        ret_ = self.MSG.msg_to(data)
                        if ret_:
                            self.reply(conn, ret_)
                        else:
                            self.reply(conn, "ERROR*LOGGING*MSG")
                        continue

                    if "MSG_OF" in data:
                        #print("[MSG_OF]:", str(data))
                        ret_ = self.MSG.msg_of(data)
                        if ret_:
                            self.reply(conn, ret_)
                        else:
                            self.reply(conn, "ERROR*LOGGING*MSG")                            
                        continue


                    #OFFLINE
                    if "OFFLINE" in data:
                        print(f'[ATTEMPT_LOGG_OFF]::{addr}::{user}\n::[DATA]::{data}')
                        self.reply(conn, "GOODBYE")
                        self.active = False
                        data_list = str(data).split("*")
                        user = str(data_list[1])
                        if len(user) >= 1:
                            self.CONTS.update_User(client, str(data_list[1]), "OFFLINE")
                            print(f"[LOGG_OFF]::{addr}::[LOGGED_OFF]::{user}::{str(data_list[1])}")
                            connections = False
                            return

                    #GET_STATE
                    if "GET_STATE" in data:
                        #print("GET_STATE::: >>")
                        data_list = str(data).split("*")
                        target_user = str(data_list[2])
                        state = self.CONTS.get_user_state(target_user)
                        state_val =  "STATE*"+str(state)
                        self.reply(conn, state_val)

                    #PROFILE_HANDLE

                    #CONTACT_LOADER
                    if "NEW_C" in data: # and self.get_conts == False:
                        try:
                            data_list = str(data).split("*")
                            if len(data_list) > 2:
                                print(f"ADDING_NEW_CONT:: for {str(data_list[1])}\nReq:: {str(data_list[2])}")
                            if data_list:
                                conts_list = self.CONTS.add_Cont(data_list)
                                if conts_list:
                                    if "NOT_FOUND*" in conts_list:
                                        print("NO SUCH USER", str(data_list[2]))
                                        self.reply(conn, "CONTS*FAIL"+str(data_list[2]))

                                    else:
                                        self.CONTS.get_conts = True
                                        self.reply(conn, "ADD_C*"+str(conts_list))
                                    continue

                            else:
                                print("[NEW_CONTS_ERROR]::")
                                self.reply(conn, "CONTS*ERROR")
                        except Exception as e:
                            print("[CONT_LOADING]::ERROR", str(e))
                    #GET_CONTACTS
                    if "CONTS" in data and get_conts == False:
                        try:
                            if "^^" in data:
                                pass
                            #print("GETTING_CONTS:: ", str(data))
                            data_list = str(data).split("*")
                            #print("USERS_LIST:: ", str(data_list))
                            if len(data_list) > 1:
                                #print("DATA_LIST:", str(data_list))
                                try:
                                    set_ = str(data_list[1])
                                    #print("[GET_CONTS]::", str(set_))
                                    if set_:
                                        conts_list = self.CONTS.Get_Contacts(set_)
                                    else:
                                        print("[FAILED]::[LOADING_CONTS]")
                                except Exception as e:
                                    print("CONTS_LIST_ERROR:: ", str(e))

                                if "EMPTY" in conts_list:
                                    print("CONTS_LIST_EMPTY")
                                    self.reply(conn, "CONTS*EMPTY%0")
                                    data_list = []
                                    get_conts = True
                                    pass

                                if "EMPTY" not in conts_list:
                                    self.reply(conn, "CONTS$"+str(conts_list))
                                    pass
                            else:
                                print("[CONTS]:[MISSING_ARGS]")
                                # MAKE REROUTE...
                                pass
                        except Exception as e:
                            #print("[CONTS_GLITCH]:: ", str(e))
                            #self.reply(conn, "CONTS*ERROR")
                            pass
                    #REGISTER
                    if "REG" in data:
                        try:
                            print("REG_NEW_USER::: ", str(data))
                            t = self.USER.Reg_User(data, client)
                            if "NEW" in t:
                                pl = self.USER.create_pl(data, client)
                                self.reply(conn, "REG_ED")
                                print('NEW_USER:: ', str(pl))
                            if "FAILED" in t:
                                self.reply(conn, "FAILED_REG")
                                print('NEW_USER:: ', str(pl))
                            if "OLD" in t:
                                self.reply(conn, "PLEASE_LOGIN")
                                print("[SENT]: PLEASE_LOGIN:: " )

                        except Exception as e:
                            print("CHECK_PLAYER::ERROR:: ", str(e))
                    #LOGIN
                    if "LOGIN" in data and self.active == False:
                        try:
                            data_list = str(data).split("*")
                            user = str(data_list[1])
                            if user:
                                print("[SETTING]_[USER] :: ", str(user))

                            t = self.USER.Login_User(data)
                            if "NEW" in t:
                                try:
                                    self.reply(conn, "PLEASE_REGISTER")
                                    print('NEW_USER:: ')
                                    pass
                                except Exception as e:
                                    print("NEW___EROOR", str(e))
                            elif "OLD" in t:
                                self.reply(conn, "LOGIN")
                                print("LOGGING_IN:: ", str(data))
                                self.active = True
                                self.USER.update_User(client, user, "ONLINE")

                                pass
                            elif "PSWD_FAIL" in t:
                                self.reply(conn, "PSWD_FAIL")
                                print("PSWD_FAIL")
                                pass
                            pass
                        except Exception as e:
                            print("CHECK_PLAYER::ERROR:: ", str(e))

                except Exception as e:
                    print('CLIENT_HANDLE_ERROR: ', str(e))
                    if user:
                        self.USER.update_User(client, user, "OFFLINE")
                        print(f"[CL_ERROR]::{addr}::[LOGGED_OFF]::{user}")
                        connections = False
                    return
                    #sys.exit(1)
            
            except Exception as e:
                print("[FAILED_TO_RECEIVE]: ", str(e))
                if user:
                    self.USER.update_User(client, user, "OFFLINE")
                    print(f"[RCV_ERROR]::{addr}::[LOGGED_OFF]::{user}")
                    connections = False

            finally:
                #print("RESETTING_LOOP")
                data = ""
                data_len = 0
                self.data = ''

        if user:
            self.USER.update_User(client, user, "OFFLINE")
            print(f"[EXT_LOOP]::{addr}::[LOGGED_OFF]::{user}")
        print("[LOOP_EXITED]:",str(user))
        return

    # THREAD CHECKER
    def check_and_join_threads(self):
        while True:
            for thread in self.threads:
                if isinstance(thread, threading.Thread) and thread.is_alive():
                    #print(str(thread), "IS_ACTIVE")
                    continue  # Thread is still active, skip it
                elif isinstance(thread, threading.Thread):
                    print(str(thread), "NOT_ACTIVE")
                    thread.join()  # Thread is no longer active, join it
                    self.threads.remove(thread)

    #MAIN_CLIENT_HANDLE
    def Main(self):
        #print("[STARTING_THREAD_CHECKER]")
        #threading.Thread(group=None, target=self.check_and_join_threads).start()


        #BIND_INCOMING_CONNECTION
        try:
            self.sock.bind(('', self.port))
            print("[BINDING] ")
        except Exception as e:
            print("NOT BINDING: ", str(e))
        #LISTEN
        try:
            # CAN CURRENTLY HANDLE 50 CLIENTS 
            self.sock.listen(50)
            print("[LISTENING]:")
        except Exception as e:
            print("[ERROR_LISTENING]", str(e))
        #CONNECTION THREADING_LOOP
        while True:
            try:
                conn, addr = self.sock.accept()
            except socket.error as e:
                print("[ERROR_CONNECTING_NEW_CLIENT] :", str(e))        
            try:
                t1 = threading.Thread(group=None, target=self.handle_client, args=(conn, addr))
                #t1.daemon = True
                t1.start()
                self.threads.append(t1)
                #print("[NEW_THREAD]:", str(t1))
            except ThreadError as e:
                print(f'SERVER::MAIN:: {str(e)}')

if __name__=="__main__":
    s = server()
    s.Main()


