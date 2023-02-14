# LOCAL IMPORTS
from file_stack_man import File_man
z
# SYS_BASE IMPORTS
import threading
import time
from datetime import datetime



class Build_Stack():
    # INITIATE VARIABLES
    def __init__(self, **kw):
        super(Build_Stack, self).__init__(**kw)
        # LOCAL
        self.FM = File_man()

        # USR
        self.verbosity          = False
        self.pre_fix            = '+27'
        self.init_seg           = '72'
        self.min_               = "2000"
        self.max_               = "9999"
        self.save_stack         = False
        self.file_name          = f"DATA2/listed_{self.init_seg}_000_.txt"

        # DT
        self.start_time         = 0
        self.end_time           = 0

        # DATA
        self.num_count          = 0
        self.saved_list_        = []
        self.checked_numbers    = []
        self.listed_numbers     = []
        self.sec_stack          = []
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

    # SAVE SEGMENT_LIST
    def save_seg_list(self, m_seg, num_list):
        try:
            dir_name = "DATA/"+str(m_seg)+"/"
            dir_check = self.FM.check_dir(dir_name)
            if dir_check == False:
                self.FM.make_dir(dir_name)
            else:
                self.FM.write_file(f"{dir_name}/listed_{m_seg}.txt", num_list, "\n", "w")
                # TODO:
                    # ADD PROFILE BASICS
                #self.FM.write_file(f"{dir_name}/listed_{m_seg}.txt", num_list, "\n", "w")

        except Exception as e:
            print(f"[E]:[SAVE_SEG_LIST]:[>{str(e)}<]")



    # CREATE PROFILE
    def create_profile(self, pre_, nsp_, mid_, tar_):
        try:
            num_ah = pre_+nsp_+mid_+tar_
            print(f"\n[NUM_@_HAND]:[{num_ah}]")
            pre_dir     = f"DATA/{str(pre_[1:])}/"
            nsp_dir     = f"{pre_dir}{nsp_}/"
            mid_dir     = f"{nsp_dir}{mid_}/"
            num_dir     = f"{mid_dir}{tar_}/"
            file_dir    = f"{num_dir}NUM.txt"
            #print(f"[PRE_DIR]:[{str(pre_dir)}][NSP_DIR]:[{nsp_dir}]\n[MID_DIR]:[{str(mid_dir)}]\n[NUM_DIR]:[{num_dir}]\n[F_FIR]:[{file_dir}]")
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
            except Exception as e:
                print(f"[E]:[CREATE_PROFILE]:[{str(e)}]")


        except Exception as tas_:
            print(f"[E]:[CREATE_PROFILE]:[{str(tas_)}]")

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
                self.num_count += 1
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




    # FULL_SET
    # LOOP mid 3 DIGITS
    def mid_seg_iter(self):
        try:
            m_seg = '000'
            for mid_ in range(1000):
                end_it = self.end_seg_iter(m_seg)
                if "ERROR" not in str(end_it):
                    self.save_seg_list(m_seg, end_it)
                    self.saved_list_.append(end_it)
                else:
                    print(f"[E]:[END_IT]:[>{str(end_it)}<]\n^[MID_ITER]")
                if self.verbosity == True:
                    print(f"[V]:[{str(self.init_seg)}_{m_seg}]:[SAVED]")

        except Exception as e:
            print(f"[E]:[mid_iter]:[>{str(e)}<]")

    # CALC TIME PER SEGMENT_LIST
    def list_numbers(self):
        time_lapse = 0
        min_lapse = 0
        sec_lapse = 0

        # GET_START_DT
        try:
            self.start_time = datetime.now()
            self.start_min_ = self.start_time.minute
            self.start_sec_ = self.start_time.second
        except:
            print('[E]:[START_TIME]:[LIST_NUMS]')

        # VERBOSE_DATA
        if self.verbosity == True:
            print(f"[START_TIME]:[>{str(self.start_min_)}:{str(self.start_sec_)}<]")
        # START TIMED LOOP
        try:
            # VERBOSE_DATA
            if self.verbosity == True:
                print("[V]:[RUNNING_BUILD]:[MID_IT]")
                print(f"[CURRENT_TIME]::{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")

            # !! #
            # START ITERATION
            self.mid_seg_iter()
            # !! #

            # CALC TIMING
            if self.verbosity == True:
                # GET_END_DT
                self.end_time = datetime.now()
                self.end_min_ = self.end_time.minute
                self.end_sec_ = self.end_time.second

                # GET_DIFF_DT
                min_lapse = self.end_min_ - self.start_min_
                sec_lapse = self.end_sec_ - self.start_sec_
                time_lapse = f"{min_lapse}:{sec_lapse}"
                print("\n[<-------------------->]\n")
                print(f"[V]:[START_TIME]:[>{str(self.start_min_)}:{str(self.start_sec_)}<]")
                print(f"[V]:[END_TIME]:[>{str(self.end_min_)}:{str(self.end_sec_)}<]")
                print(f"[V]:[TIME_LAPSE]:[>{time_lapse}<]")

            # COMPLETE_BUILD
            print(f"\n[BUILD]::[COMPLETE]::\
                    \n    [TIME]:[H:M:S]->[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}]\
                    \n    [NUM_COUNT]->[{self.num_count}]\
                    \n")
        except Exception as e:
            print(f"[E]:[list_nums]:[>{str(e)}<]")

    # CREATE ALL SEGMENTS
    def all_segs(self):
        try:
            for seg_ in self.init_segs:
                print(f"[CURRENT_SEG]:@:[>{str(seg_)}<]")
                self.init_seg = seg_
                self.list_numbers()
        except Exception as e:
            print(f"[E]:[ALL_SEG_]:[>{str(e)}<]")

    # RUN BUILD PARAMETERS
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
            print("[STARTING_BUILD]")
            # RUN_BUILD_ 

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
            if "*" in str(init_seg_):
                print("[ALL_NSP]")
                self.all_segs()
                save_list_ = self.save_list_
                return saved_list_


        except Exception as m:
            print(f"[E]:[M]:[Build_Stack]:[>{str(m)}<]")







# +27 40 00 8391
# +27 72 072 6777
