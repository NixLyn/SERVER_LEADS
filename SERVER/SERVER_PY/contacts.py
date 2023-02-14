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


    from BASE_PY import *

except Exception as e:
    print(f"[E]:[{str(e)}]")


class Conts_():
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



    #GET_CONTACT_LIST
    def Get_Contacts(self, user):

        file_name = ""
        user_file = ""
        data_up = []
        user_conts = []
        p_u = ""
        u_q = ""
        u_dt = ""
        up_cont = ""
        f_u = []
        conts_lst_str = ""

        stats_ = ""

        try:
            file_name = "CONTS/"+user+".txt"
            user_file = self.FM.check_file(file_name)
            
            if user_file == True:
                user_conts = self.FM.read_file(file_name, "%")
                if len(user_conts) > 0 and type(user_conts) == list:
                    try:
                        # FRST CHECK STATUS AND UPDATE TO USE THE CURRENT TIME
                        #   get_user_state
                        for u in user_conts:
                            #print("\n\nUSER_IN_QU: ", str(u))
                            if not u:
                                pass
                            try:
                                p_u = str(u)
                                f_u = p_u.split("@")
                                if len(f_u) > 1:
                                    u_q = str(f_u[0])

                                # u_q = str(p_u.split("@")[0])
                                # print("\nGET_USER_STATUS->: ", u_q)



                    # BUG_HERE -....>


                                if u_q:
                                    u_dt = self.get_user_state(u_q)
                                    #print("[U_DT]::", u_dt)
                                    if u_dt:
                                        stats_ = u_q+"*"+u_dt
                                    #print("[STAT]:", str(stats_))
                            except Exception as e:
                                print("[GET_USER_ERROR]:[?]:", str(e), "[WHAT???!!!]::", )

                            if stats_:
                                try:

                                    #print("[CONT]:: ", str(stats_))
                                    if stats_ not in str(data_up):
                                        data_up.append(stats_)
                                except Exception as e:
                                    print("[ERROR]::[GET_CONTS]::[STATUS]::", str(e))
                        try:
                            conts_lst_str = self.lst_to_str(data_up, "%")
                        except:
                            pass
                        #print("CONTS:: ", str(conts_lst_str))

                        return conts_lst_str
                    except Exception as e:
                        print("RET_LIST_ERROR:: ", str(e))
                else:
                    print("CONTS_EMPTY", str(conts_lst_str))
                    return "EMPTY"

        except Exception as c_u:
            print("_ERROR::GET_CONTACTS:: ", str(c_u))

    # ADD_CONTACT
    def add_Cont(self, data):
        #data[0] = act
        #data[1] = user
        #data[2] = new_cont
        user_f_name = "CONTS/"+str(data[1])+".txt"
        new_cont_f_name = "CONTS/"+str(data[2])+".txt"
        msgs_d_name = "MSGS/"+str(data[1])
        chat_f_name = "MSGS/"+str(data[1])+"/"+str(data[2])+".txt"

        user_file = "USERS/"+str(data[2])+".txt"

        print(f"@-[ADD_CONTS]::\n\
                >>[U_F_NAME]:       [{user_f_name}]\n\
                >>[NEW_C_F_NAME]:   [{new_cont_f_name}]\n\
                >>[MSG_D_NAME]:     [{msgs_d_name}]\n\
                >>[CHAT_F_NAME]:    [{chat_f_name}]\n\
                >>[USER_FILE]:      [{user_file}]\n\
                ")

        is_user = self.FM.check_file(user_file)
        #print("[CHECKING_FILE]::", str(user_file))
        if is_user != True:
            print("[USER_NOT_FOUND]")
            return "NOT_FOUND"
        else:
            print("[FETCHING_DATA]::", str(data[2]))


        #print("data[2]:: ", str(data[2]))
        new_cont_c = self.FM.check_file(new_cont_f_name)
        if new_cont_c == True:
            try:
                #GET_OLD_LIST
                c_list = self.FM.read_file(user_f_name, "%")
                #print("C_LIST:: ", str(c_list))
                #CHECK IF ALREADY THERE
                n_list = []
                if str(data[2]) in c_list:
                    print("KHONA") # CONTACT ALREADY EXISTS
                    return "KHONA"
                if len(c_list) > 0: 
                    for _ in c_list:
                        if "EMPTY" not in str(_) and len(_) > 0: # IF THERE ARE CONTACTS (NOT_EMPTY)
                            n_list.append(str(_))
                            print("ADDING TO NEW LIST:: ", str(_), "\n\
                            *******************************")

                if str(data[2]) not in str(n_list): # IF CONT IN QUESTION NOT IN LIST 
                    n_list.append(str(data[2])+"@OFFLINE") # ADD TO LIST  
                                                    # BUT ADD THE STATUS OF THAT CONT, FIRST AS 
                                                            # OFFLINE, UPDATE ON REFRESH (GET_CONTS)
                    print("N_LIST:: ", str(n_list))
                    try:
                        self.FM.write_file(user_f_name, n_list, "%", "w")
                    except Exception as e:
                        print(f"[E]:[ADD_TO_CONTS_FILE]:[{str(e)}]")
                    # CREATE CHAT DIRECTORY
                    try:
                        is_dir = self.FM.check_dir(msgs_d_name)
                        if is_dir == False:
                            self.FM.make_dir(msgs_d_name)
                    except Exception as e:
                        print(f"[E]:[CREATING_DIR]:[{str(e)}]")
                    try:
                        self.FM.write_file(chat_f_name, str(data[2])+"*", "&", "w")
                    except Exception as e:
                        print(f"[E]:[ADD_TO_CHATS_FILE]:[{str(e)}]")

                    return str(n_list)
            except Exception as e:
                print("ADDING_CONT_ERROR", str(e))

    #GET_STATUS
    def get_user_state(self, user):
        #TARGET_USER...
        #print("GET_USER_STATE:: ", str(user))

        now = datetime.now()
        # Format the date and time as a string in the desired format
        date_time_str = now.strftime("%Y-%m-%d-%H-%M-%S")

        f_name = "USERS/"+str(user)+".txt"
        user_data = self.FM.read_file(f_name, "*")
        last_seen = ""

        use_less = ""
        status_ = ""
        ret_val = ""

        if len(user_data) >= 6:
            for i, u_ in enumerate(user_data):
                #print("[WTF::]::", str(i),"::",str(u_), "<--")
                if i == 3:
                    last_seen = str(u_)
                    #print("LAST_SEEN:: ", str(u_))
                if i == 4:
                    status_ = str(u_)
                    #print("STATUS:: ", str(u_))

            ret_val = last_seen+"*"+status_
            #print("[GET_STATUS]::[RET_VAL]::", ret_val)
            return ret_val
