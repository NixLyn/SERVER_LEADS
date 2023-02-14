# SYS_BASIC IMPORTS
import threading
import time
from datetime import datetime


from STACK_PY import file_stack_man, phone_vali_, trucall_scan, web_stack, geo_stat

class Get_Stack():
    # INITIATE VARIABLES
    def __init__(self, **kw):
        super().__init__(**kw)
        # LOCAL
        from STACK_PY.file_stack_man import File_man
        #from file_stack_man import File_man
        self.FM                 = File_man()

        # STACK IMPORTS
        from STACK_PY.trucall_scan import TrueCallerScan
        self.TR_JS            = TrueCallerScan()

        from STACK_PY.web_stack import Web_Stack
        self.WS             = Web_Stack()

        from STACK_PY.phone_vali_ import NumPho
        self.NP                 = NumPho()



        # USER_DEFINE
        self.verbosity          = False
        self.pre_fix            = '+27'
        self.init_seg           = '72'
        self.save_stack         = False
        self.file_name          = f"USER_DEFINED/listed_{self.init_seg}_000_.txt"
        self.final_list         = []

        # SEARCH OPTS
        self.tcj_               = False
        self.url_               = False

        # RUN_TIME
        self.start_time         = 0
        self.end_time           = 0

        # DATA
        self.get_list_          = []
        self.seg_list           = []
        self.checked_numbers    = []
        self.listed_numbers     = []
        self.init_segs = [
                        '40',  # 0/    # EastCape, WestCape
                        '41',  # 1
                        '42',  # 2
                        '43',  # 3
                        '44',  # 4
                        '45',  # 5
                        '46',  # 6
                        '47',  # 7
                        '48',  # 8
                        '49',  # 9
                        '51',  # 10    # NorthCape, FreeState
                        '53',  # 11
                        '54',  # 12
                        '56',  # 13
                        '57',  # 14
                        '58',  # 15
                        '60',  # 16    # Cellular: 1
                        '61',  # 17
                        '62',  # 18
                        '63',  # 19
                        '64',  # 20
                        '65',  # 21
                        '66',  # 22
                        '67',  # 23
                        '68',  # 24
                        '69',  # 25
                        '71',  # 26    # Cellular: 2
                        '72',  # 27
                        '73',  # 28
                        '74',  # 29
                        '76',  # 30
                        '78',  # 31
                        '79',  # 32
                        '81',  # 33    # Cellular: 3
                        '82',  # 34
                        '83',  # 34
                        '84'   # 35
                        ]


    # GET SEGMENT_LIST
    def get_seg_list(self, m_seg):
        try:
            if m_seg == "000":
                return
            dir_name = "STACK_PY/DATA/"+str(self.init_seg)
            dir_check = self.FM.check_dir(dir_name)
            if dir_check == False:
                self.FM.make_dir(dir_name)
            else:
                ret_list = self.FM.read_file(f"{dir_name}/listed_{m_seg}.txt", "\n")
                if ret_list:
                    return ret_list
        except Exception as e:
            print(f"[E]:[GET_SEG_LIST]:[>{str(e)}<]")


    # DECORATE SEGMENT_LIST WITH PREFIX
    def dress_stack(self):
        try:
            temp_ = ""
            #print(f"[SEG_LIST]_@_[HAND]\n>>[>{str()}<]")
            for i, val in enumerate(self.seg_list):
                #print("[VAL]:", str(val))
                if str(val) == "000":
                    continue
                temp_= self.pre_fix+self.init_seg+val.replace("\n", "")
                #print("[TEMP_]", str(temp_))
                self.get_list_.append(temp_)
                tVal = str(val).replace("\n", "")
            
            #self.final_list.append(self.seg_list)
            #self.seg_list = []


        except Exception as e:
            print(f"[E]:[DRESS]:[>{str(e)}<]")


    # SAVE SEGMENT_lIST (UPDATE?)
    def stack_save(self, mid_seg):
        try:
            #self.FM.make_dir(f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_{datetime.now().second}")
            self.FM.make_dir("STACK_PY/SAVE_STACK")
            self.FM.write_file(f"STACK_PY/SAVE_STACK/saved_{str(self.init_seg)}_{str(mid_seg)}.txt", self.seg_list, "\n", "w")
        except Exception as e:
            print(f"[E]:[stack_save]:[>{str(e)}<]")
            if "Errno 17" in str(e):
                print("[SEGMENT_LIST]:[ALREADY_BUILT]")
                return 1

    # LOOP SEGMENT_LIST RANGE
    def get_stack(self):
        try:
            stack_set = []
            m_seg = '000'
            for mid_ in range(1000):
                if mid_ < 10:
                    m_seg = '00'+str(mid_)
                elif mid_ < 100:
                    m_seg = '0'+str(mid_)
                elif mid_ < 1000:
                    m_seg = str(mid_)
                if self.verbosity == True:
                    print(f"[MID_SEG]:[>{m_seg}<]")

                # PULL FILE DATA OF EACH MID_SEG
                self.seg_list = self.get_seg_list(m_seg)

                # DRESS WITH PREFIX & NSP_N
                self.dress_stack()


        except Exception as e:
            print(f"[E]:[get_stack]:[>{str(e)}<]")

    # COLLECT ALL
    def all_segs(self):
        try:
            for seg_ in self.init_segs:
                print(f"[FETCHING]:[>{str(seg_)}<]")
                self.init_seg = str(seg_)
                self.get_stack()
        except Exception as e:
            print(f"[E]:[ALL_SEGS]:[>{str(e)}<]")





    # SEARCH PROFILE
    def create_profile(self, pre_, nsp_, mid_, tar_):
        try:
            tr_scan     = []
            name_       = ""
            email_      = ""

            num_ah      = pre_+nsp_+mid_+tar_
            pre_dir     = f"STACK_PY/DATA/{str(pre_[1:])}/"
            nsp_dir     = f"{pre_dir}{nsp_}/"
            mid_dir     = f"{nsp_dir}{mid_}/"
            num_dir     = f"{mid_dir}{tar_}/"
            num_file    = f"{num_dir}NUM_.txt"
            file_dir    = f"{num_dir}NUM.txt"
            name_dir    = f"{num_dir}NAME.txt"
            mail_dir    = f"{num_dir}MAIL.txt"

            # CLEAN SEARCH
            urls_dir    = f"{num_dir}URLS.csv"

            # DORKS
            fb_file    = f"{num_dir}FB_DORK.csv"
            tw_file    = f"{num_dir}TW_DORK.csv"
            li_file    = f"{num_dir}LI_DORK.csv"
            in_file    = f"{num_dir}IN_DORK.csv"



            print(f"\n[NUM_@_HAND]:[{num_ah}]")

            # TRUE_CALLER_SCAN
            try:
                is_pre = self.FM.check_dir(pre_dir)
                if is_pre == False:
                    self.FM.make_dir(pre_dir)
                is_nsp = self.FM.check_dir(nsp_dir)
                if is_nsp == False:
                    self.FM.make_dir(nsp_dir)
                is_mid = self.FM.check_dir(mid_dir)
                if is_mid == False:
                    self.FM.make_dir(mid_dir)
                is_num_ = self.FM.check_dir(num_dir)
                if is_num_ == False:
                    self.FM.make_dir(num_dir)
                    self.FM.write_file(file_dir, str(num_ah), ",", "a+")

                # TRUE_CALLER_SCAN
                name_check = self.FM.check_file(name_dir)
                if name_check == False:
                    print("[NO_NAME]:[SCANNING_NOW]")
                    try:
                        got_name = self.FM.check_file(name_dir)
                        if got_name == False:
                            tr_scan = self.TR_JS.get_data(num_ah)
                            if "NONE" not in str(tr_scan[0]):
                                name_ = str(tr_scan[0])
                                self.FM.write_file(name_dir, name_, ",", "a+")
                            if "NONE" not in str(tr_scan[1]):
                                email_ = str(tr_scan[1])
                                self.FM.write_file(mail_dir, email_, ",", "a+")
                    except Exception as e:
                        print(f"[E]:[TRUE_SCAN]:[{str(e)}]")


                num_look_ = self.FM.check_file(num_file)
                if num_look_ == False:
                    try:
                        da_num_ = self.NP.check_num_data_(num_ah)
                        if "NONE" not in str(da_num_):
                            self.FM.write_file(num_file, da_num_, ",", "a+")
                    except Exception as e:
                        print(f"[E]:[TRUE_SCAN]:[{str(e)}]")


                try:
                    g_rl_ = f'https://www.google.com/search?client=firefox-b-e&q={num_ah}'
                    urls_ = self.WS.scrape_url(g_rl_)
                    if urls_:
                        is_url_ = self.FM.check_file(urls_dir)
                        if is_url_ == False:
                            self.FM.write_file(urls_dir, str(urls_), "\n", "a+")
                except Exception as e:
                    print(f"[E]:[PROFILE_URLS]:[{str(e)}]")
            except Exception as e:
                print(f"[E]:[SCRAPE_PROFILE]:[{str(e)}]")


            # DORK_STACK
            try:
                # FACE_BOOK
                try:
                    fb_dork_ = self.WS.fb_dork_(num_ah)
                    if "NOT_FOUND" not in str(fb_dork):
                        self.FM.write_file(fb_file, fb_dork_, ",", "a+")
                    else:
                        print("NO_FB")
                except Exception as e:
                    print(f"[E]:[GET_FB]:[{str(e)}]")

                # TWITTER
                try:
                    tw_dork_ = self.WS.tw_dork_(num_ah)
                    if "NOT_FOUND" not in str(tw_dork):
                        self.FM.write_file(tw_file, tw_dork_, ",", "a+")
                    else:
                        print("NO_TW")
                except Exception as e:
                    print(f"[E]:[GET_TW]:[{str(e)}]")


                # LINKED_IN
                try:
                    li_dork_ = self.WS.li_dork_(num_ah)
                    if "NOT_FOUND" not in str(fb_dork):
                        self.FM.write_file(li_file, li_dork_, ",", "a+")
                    else:
                        print("NO_LI")
                except Exception as e:
                    print(f"[E]:[GET_LI]:[{str(e)}]")


                # INSTAGRAM
                try:
                    in_dork_ = self.WS.in_dork_(num_ah)
                    if "NOT_FOUND" not in str(fb_dork):
                        self.FM.write_file(in_file, in_dork_, ",", "a+")
                    else:
                        print("NO_IN")
                except Exception as e:
                    print(f"[E]:[GET_FB]:[{str(e)}]")
            except Exception as e:
                print(f"[E]:[SCRAPE_PROFILE]:[{str(e)}]")


        except Exception as e:
            print(f"[E]:[CREATE_PROFILE]:[{str(e)}]")






    # SPECIFIED NSP
    # LOOP LAST 4 DIGITS
    def end_seg_iter(self, pre_, nsp_, mid_seg):
        try:
            print(f"[PRE_]::[{str(pre_)}]")
            print(f"[NSP_]::[{str(nsp_)}]")
            print(f"[MID_]::[{str(mid_seg)}]")

            save_list       = []
            end_seg         = '0000'
            for j in range(10000):
                if j < 10:
                    end_seg = '000'+str(j)
                elif j < 100:
                    end_seg = '00'+str(j)
                elif j < 1000:
                    end_seg = '0'+str(j)
                elif j <= 9999:
                    end_seg = str(j)

                tar_number = nsp_+mid_seg+end_seg
                save_list.append(tar_number)
                self.create_profile(pre_, nsp_, mid_seg, end_seg)

            return save_list
        except Exception as e:
            print(f"[E]:[end_seg_iter]:[>{str(e)}<]")
            return ["ERROR:", str(e)]

    # LOOP mid 3 DIGITS
    def sec_seg_iter(self, min_, max_, pre_, nsp_):
        try:
            min_n_          = int(min_)
            max_n_          = int(max_)
            sec_stack       = []
            m_seg           = '000'
            sec_len         = 0

            for mid_ in range(1000):
                if mid_ >= min_n_ and mid_ <= max_n_:
                    if len(str(mid_)) == 1:
                        m_seg = '00'+str(mid_)
                    elif len(str(mid_)) == 2:
                        m_seg = '0'+str(mid_)
                    elif len(str(mid_)) == 3:
                        m_seg = str(mid_)
                    elif len(str(mid_)) >= 4:
                        break

                    end_it = self.end_seg_iter(pre_, nsp_, str(m_seg))
                    if "ERROR" not in str(end_it):
                        self.sec_stack.append(end_it)
                        sec_stack.append(end_it)
                    else:
                        print(f"[E]:[END_IT]:[>{str(end_it)}<]\n^[MID_ITER]")
                if self.verbosity == True:
                    print(f"[V]:[{str(self.init_seg)}_{m_seg}]:[SAVED]")
            
            sec_len = len(sec_stack)

            print(f"[CURRENT_TOT]:[<<{str(sec_len)}>>]\n<<-------------------->>")
        except Exception as e:
            print(f"[E]:[sec_seg_iter]:[>{str(e)}<]\n[E_@]:[<{str(nsp_)}>]")
            return ["ERROR:", str(e)]

    # SPECIFIED NSP
    def nsp_seg_iter(self, min_, max_,  pre_, nsp_):
        try:
            print(f"[ITER]_@_[{str(nsp_)}]")
            list_saved_ = self.sec_seg_iter(min_, max_, pre_, nsp_)
            return list_saved_

        except Exception as e:
            print(f"[E]:[nsp_seg_iter]:[>{str(e)}<]\n[E_@]:[<{str(nsp_)}>]")
            return ["ERROR:", str(e)]







    # PROMPT PARAMETERS FOR BUILD
    def main_(self, prefix_, init_seg_,  min_, max_, save_stack_, verbosity_):
        try:
            self.prefix         = prefix_
            self.init_seg       = init_seg_
            self.save_stack     = save_stack_
            self.min_           = min_ 
            self.max_           = max_
            self.verbosity_     = verbosity_
            saved_list_         = []



            print(f"[CURRENT_TIME]::[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]")
            # DEFAULT_CHECK
            print(f"[STARTING_SEARCH]\n>>>[TRUCALLER_SCAN][{str(self.tcj_)}]\n>>[URL_SCAN]:[{str(self.url_)}]\n")
            # RUN_SEARCH_ 

            print(f"[{str(init_seg_)}]")

            if str(init_seg_) in str(self.init_segs): # and "*" not in str(init_seg_):
                print(f"[SPECIFIED_NSP]:[{str(init_seg_)}]")
                if str(init_seg_) not in str(self.init_segs):
                    return "B_ERROR*INIT_SEGS*"
                else:
                    try:
                        print(f"[S_NSP_BUILDING...]:[{prefix_}, {init_seg_}, {min_}, {max_}]")
                        saved_list_ = self.nsp_seg_iter(min_, max_, prefix_, init_seg_)
                        print(f"[nUM_TOT]:[{str(len(saved_list_))}]")
                        return saved_list_
                    except Exception as sf:
                        print(f"[E]:[S_NSP]:[{str(sf)}]")
            #if "*" in str(init_seg_):
            #    print("[ALL_NSP]")
            #    self.all_segs()
            #    save_list_ = self.save_list_
            #    return saved_list_






        except Exception as m:
            print(f"[E]:[M]:[Build_Stack]:[>{str(m)}<]")
