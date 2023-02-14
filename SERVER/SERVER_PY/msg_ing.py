try:
    # LOCAL
    from BASE_PY import *

    # STD
    import socket
    import string
    import sys
    from threading import Thread, ThreadError
    import threading
    from datetime import datetime
except Exception as e:
    print(f"[E]:[{str(e)}]")


class Msgs_():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # BASE_PY
        from BASE_PY.File_Man import File_man
        self.FM         = File_man()


    #CLEAN DATA - LIST-->>STR
    def lst_to_str(self, data_lst, delim):
        try:
            data_str = ""
            #print("LIST_TO_STR:: ", str(data_lst))
            if type(data_lst) == list:
                #print("CONVERTING")
                for _ in data_lst:
                    data_str += str(_)+str(delim)

                #print("LST_TO_STR", data_str)
            return data_str
        except Exception as e:
            print("LIST_TO_STR:[ERROR]:: ", str(e))



    # MESSAGING
    # SAVE MSGS
    def msg_to(self, data):
        ###
        #	|-MSGS/
    	#    	|-User1/
    	#   		|-User2.txt -> "<date_time_1>$<msg_1>$<received_1>$&<date_time_2>$<msg_2>$<received_2>$&"

        file_name = ""
        to_user = ""
        of_user = ""
        the_msg = ""
        to_send =  ""
        check_file =  False
        ret_ = ""

        #print("\n\n[MSG_TO]\n>>>", str(data))
        break_msg = data.split("*")
        if len(break_msg) > 3:
            #print("TO : ", str(break_msg[1]))
            to_user = str(break_msg[1])
            #print("OF : ", str(break_msg[2]))
            of_user = str(break_msg[2])
            #print("MSG: ", str(break_msg[3]))
            the_msg = str(break_msg[3])

            # DATE_TIME_STAMP
            # Get the current date and time
            now = datetime.now()

            # Format the date and time as a string in the desired format
            date_time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
            to_send = "*"+date_time_str+"*"+the_msg+"&"
            #print("TO_SAVE:: ", str(to_send))
            file_name = "MSGS/"+to_user+"/"+of_user+".txt"
            #print("FILE-> ", str(file_name))

        check_file = self.FM.check_file(file_name)
        if check_file == True:
            #print("[ACCESS_GRANTED]")
            self.FM.write_file(file_name, to_send, "\n", "a")
            ret_ = "MSG*SAVED*"+to_user+"*"+to_send+"*"
            return ret_

        else:
            print("[ACCESS_DENIED]")
            return "MSG*ACCESS_DENIED*"+to_user+"*"+to_send+"*"

    # COLLECT MSGS && REORDER BY DATE_TIME
    def msg_of(self, data):

        print("MSG_OF:: ", str(data))
        try:

            dataLs = data.split("*")
            ret_lst = []
            set_lst = []
            sorted_msgs = []
            ret_str = ""

            dir_of = "MSGS/"+str(dataLs[1])+"/"     # USER SENDING REQUEST
            dir_to = "MSGS/"+str(dataLs[2])+"/"     # USER CONTACT

        except Exception as e:
            print(f"[E]:[MSG_OF]:[{str(e)}]")


        try:
            if len(dataLs) >= 3:
                # COLLECT ALL MSGS
                file_name = dir_of+str(dataLs[2])+".txt"
                msg_from = self.FM.read_file(file_name, "&")
                print("[MSG_FROM]:", str(msg_from))
                if len(msg_from) > 0:
                    for m_ in msg_from:
                        n_ = m_.split("*")
                        if len(n_) < 3:
                            #print("[NOT_MSG]", str(n_))
                            continue
                        else:
                            ret_lst.append(str(dataLs[2]) + "*" + str(m_) + "&")
                            #print("[G]:[MSG_OF]:", str(dataLs[2]) + "*" + str(m_) + "&")
                else:
                    print("\n[EMPTY_MSG_BLOCK]",str(msg_from))

                # CELLECT SENT MSGS
                my_file = dir_to+str(dataLs[1])+".txt"
                msg_to = self.FM.read_file(my_file, "&")

                if  len(msg_to) > 0:
                    for m_ in msg_to:
                        n_ = m_.split("*")
                        if len(n_) < 3:
                            #print("[NOT_MSG]", str(n_))
                            continue
                        else:
                            ret_lst.append(str(dataLs[1]) + "*" + str(m_) + "&")
                            #print("[G]:[MSG_TO]:", str(dataLs[1]) + "*" + str(m_) + "&")
                else:
                    print("\n[EMPTY_MSG_BLOCK]",str(msg_to))
                try:
                    for i, il in enumerate(ret_lst):
                        i_s = str(il).split("*")
                        #print("[I]:", str(i))
                        set_lst.append(i_s)
                    sorted_msgs = sorted(set_lst, key=lambda x: x[2])
                    for i in sorted_msgs:
                        #print("[SORTED]:: -->> ", str(i))
                        ret_str += self.lst_to_str(i, "*")+"$"
                    return "MSGS_OF*"+ str(dataLs[2])+"@"+ret_str
                except Exception as e:
                    print("[USELESS]:->>",str(e))
                    return str(["MSGS&", "NO&","MSGS&"])

            else:
                 return "MSGS&ERROR"

        except Exception as e:
            print(f"[E]:[MSG_OF]:[{str(e)}]")











