






class JuncK():
    def __init__():
        pass

    # LOOP GEO_LIST
    # ToDo:
        # APPLY OpenCage_API_KEY
        # PROMPT_API_KEY
    def geo_scan(self):
        try:
            for num in self.current_stack:
                # Create Profile (Folder) for number
                f_name = str(str(num).replace("+", ""))
                num_dir = "TAP_DATA/PROFILES/"+f"NUM_{f_name}"
                self.FM.make_dir(num_dir)
                # Set Profile
                num_prof = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/PROFILE.csv"
                geo_ = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/GEO_.txt"
                urls_ = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/URLS_.txt"
                self.FM.write_file(num_prof, "Number, "+str(num), "\n", "w")


                #check_geo_ = self.FM.check_file(geo_)
                #if check_geo_ == False:
                try:
                    if self.geo_count <= 500:
                        geo_stat = self.GEO.check_number(num)
                        self.FM.write_file(geo_, geo_stat, "\n", "w")
                        self.geo_count+=1
                        # UPDATE PROFILE.csv
                except:
                    # UPDATE PROFILE
                    pass
                else:
                    print(f"[GEO_PRESET]:[>{str(num)}<]")
        except Exception as e:
            print(f"[E]:[GEO_SCAN]:[>{str(e)}<]")

    # LOOP URL_SCAN
    # ToDo:
        # CHECK G_DORKS:
            # NUMBER
            # NAME
            # EMAIL
    def url_scan(self, param_):
        try:
            for num in self.current_stack and num >= param_:
                f_name = str(str(num).replace("+", ""))

                # GET NUMB_URLS
                if numb_ == True:
                    # FETCH_NAME
                    try:
                        numb_furl = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/NUMB_URL.csv"
                        numb_url = self.WS.search_it(num)
                        self.FM.write_file(numb_furl, numb_url, "\n", "w")
                    except:
                        pass

                # GET NAME_URLS
                if name_ == True:
                    try:
                        # FETCH_NAME
                        name_ = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/NAME_.csv"
                        g_name = self.FM.read_file(name_, "\n")
                        try:
                            # FETCH_URLS_->_NAME
                            name_furl = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/NAME_URL.csv"
                            name_url = self.WS.search_it(g_name)
                            self.FM.write_file(name_, name_furl, "\n", "w")
                        except:
                            pass
                    except:
                        pass


                # GET EMAIL_URLS
                if email_ == True:
                    # FETCH_NAME
                    try:
                        name_ = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/MAIL_.csv"
                        g_name = self.FM.read_file(name_, "\n")
                        try:
                            name_furl = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/MAIL_URL.csv"
                            name_url = self.WS.search_it(g_name)
                            self.FM.write_file(name_, name_furl, "\n", "w")
                        except:
                            pass
                    except:
                        pass

                try:
                    mail_of = self.TCS.get_email(num)
                    self.FM.write_file(email_, mail_of, "\n", "w")
                except:
                    pass
        except Exception as e:
            print(f"[E]:[URL_SCAN]:[>{str(e)}<]")

    # LOOP GET_CALLER
    # APPLY TRUECALLER_LOGIN_KEY
    def nn_scan(self, param_):
        try:
            num_        = 0
            stack_      = []
            found_      = ""

            for num in self.current_stack:
                # Create Profile (Folder) for number
                f_name = str(str(num).replace("+", "")[-6:])
                u_name = str(str(num).replace("+", ""))

                num_dir = "TAP_DATA/PROFILES/"+f"NUM_{f_name}"

                if not self.FM.check_dir(num_dir):
                    self.FM.make_dir(num_dir)
                    # Set Profile

                profile_f = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/PROFILE_.csv"
                self.FM.write_file(profile_f, )

                pall_f = "TAP_DATA/PROFILES/"+f"NUM_{f_name}/PALL_.csv"

                # GET P_ALL
                try:
                    if num_ >= int(param_):
                        print(f'[NUM]:[{num_}]\n[{str(param_)}]')
                        pall_of = self.TCS.get_pall(num)
                        if "Please try again" not in str(pall_of):
                            self.FM.write_file(pall_f, f"[{num_}],"+str(pall_of), "\n", "w")
                            found_ = f"[{num_}]:[{u_name}]:[{str(pall_of)}]"
                            stack_.append(pall_of)
                            num_+=1
                        else:
                            break
                except Exception as e:
                    stack_.append(f"[TRS_ERROR]:[{str(e)}]")
                    return stack_
            return stack_

        except Exception as e:
            print(f"[E]:[TRUE_CALLER_SCAN]:[>{str(e)}<]")

