
try:
    # STD
    import socket
    import string
    import sys
    from threading import Thread, ThreadError
    import threading
    from datetime import datetime



    # LOCAL
    from SERVER_PY import *
    from SERVER_PY.File_User_Man import File_man


except Exception as e:
    print(f"[E]:[{str(e)}]")


class Users_():
    def __init__(self, **kwargs):
        super(Users_, self).__init__(**kwargs)
        from SERVER_PY.File_User_Man import File_man

        # BASE_PY
        self.FM         = File_man()


    #PROFILE_UPDATE
    def update_User(self, client, user, state):
        # ->get_file_data -> fileter to list
        # data[0] = action
        # data[1] = USER

        #USER_FILE::
        #   >[0] = action
        #   >[1] = user_name
        #   >[2] = pswd
        #   >[3] = client_data....(NOT_NOW){TO_MUCH_BS}
        #   >[4] = status
        #   >[5] = contact_list{FILE_NAME}
        #   >[6] = msgs{FILE_NAME} : delim = "%"


        try:
            now = datetime.now()
            # Format the date and time as a string in the desired format
            date_time_str = now.strftime("%Y-%m-%d-%H-%M-%S")


            if "OFFLINE" in state:
                print(f"[UPDATE_USER]::{str(user)}::[OFFLINE]")
            if not user:
                return

            f_name = "SERVER_PY/USERS/"+str(user)+".txt"
            user_data = self.FM.read_file(f_name, "*")
            # user_data[4] = ONLINE/OFFLINE
            user_update = []
            #print(f"LEN(USER_DATA) > {str(len(user_data))}")
            if len(user_data) >= 6:
                for i, _ in enumerate(user_data):
                    if _ and i != 4 and i != 3:
                        user_update.append(str(_))
                    if i == 3:
                        user_update.append(str(date_time_str))
                    if i == 4:
                        user_update.append(str(state))
                self.FM.write_file(f_name, user_update, "*", "w")



        except Exception as r:
            print("USER_UPDATE_ERROR: ", str(r))

    #LOGIN
    def Login_User(self, data):
        try:
            print("ATTEMPTING_LOGIN:: ", str(data))
            user = data.split("*")
            if len(user) >= 3:
                User = str(user[1]).translate(str.maketrans('','',string.punctuation))
                PSWD = str(user[2]).translate(str.maketrans('','',string.punctuation))
                print("USER   ::", User)
                print("PSWD   ::", PSWD)
                file_name = "SERVER_PY/USERS/"+User+".txt"

                try:
                    f_ret = self.FM.check_file(file_name)
                except Exception as e:
                    print("CHECK_FILE_ERROR", str(e))

                if f_ret != True:
                    print("USER_NOT FOUND")
                    return "NEW"
                elif f_ret == True:
                    print("F_RET", str(f_ret))
                    f_data = self.FM.read_file(file_name, "*")
                    #print("F_DATA:: ", str(f_data), "\nLEN:: ", str(len(f_data)))
                    if len(f_data) >= 3:
                        f_User = str(f_data[1])
                        f_pswd = str(f_data[2])
                        if str(f_pswd) == str(PSWD) and str(f_User) == str(User):
                            print("WELCOME_BACK: ", str(User))
                            return "OLD"
                        elif str(f_pswd) != str(PSWD) and str(f_User) == str(User):
                            print("CHECK_USER_ERROR")
                            return "PSWD_FAIL"
        except Exception as e:
            print("CHECK_USER_ERROR::: ", str(e))
            return "PSWD_FAIL"

    #REGISTER
    def Reg_User(self, data, client):
        try:
            print("ATTEMPTING_REGISTER:: ", str(data))
            user = data.split("*")
            if len(user) > 1:
                User = str(user[1]).translate(str.maketrans('','',string.punctuation))
                print("USER   ::", User)
                file_name = "SERVER_PY/USERS/"+User+".txt"
                f_ret = self.FM.check_file(file_name)
                if f_ret != True:
                    print("USER_NOT FOUND")
                    try:
                        return "NEW"
                    except Exception as e:
                        print("[FAILED_TO_REGISTER_USER]:", str(data), "\n>>", str(e))
                        return "FAILED"

                else:
                    print("WELCOME_BACK", str(User))
                    return "OLD"


        except Exception as e:
            print("CHECK_USER_ERROR::: ", str(e))

    #CREATE_USER_FILE
    def create_pl(self, data, client):
        #USER_FILE:: 
        #   >[0] = action
        #   >[1] = user_name
        #   >[2] = pswd
        #   >[3] = client_data....(NOT_NOW){TO_MUCH_BS}
        #   >[4] = status
        #   >[5] = contact_list{FILE_NAME}
        #   >[6] = msgs{FILE_NAME} : delim = "%"

        #print("CHECKING_USER", data)
        user = data.split("*")
        User = str(user[1]).translate(str.maketrans('','',string.punctuation))
        PSWD = str(user[2]).translate(str.maketrans('','',string.punctuation))

        try:
            file_name = "SERVER_PY/USERS/"+User+".txt"
            msgs_folder = "SERVER_PY/MSGS/"+User
            contacts_file = "SERVER_PY/CONTS/"+User+".txt"
            new_ = "USER*"+User+"*"+PSWD+"*"+"__CLIENT__"+"*"+"ONLINE"+"*"+contacts_file+"*"+msgs_folder+"*"
            print("NEW__:: ", str(new_))
            self.FM.make_dir(msgs_folder)
            self.FM.write_file(file_name, new_, "*", "w")
            self.FM.write_file(contacts_file, "EMPTY", "%", "w")
            return new_
        except Exception as e:
            print("CREATE_USER_ERROR:", str(e))
            return "FAIL"





