# SYS_BASE IMPORTS
import threading
import time
from datetime import datetime
import sys
import os



from STACK_PY import *
#from STACK_PY.file_handle import File_man

class Stack_Opt():
    def __init__(self, **kw):
        super(Stack_Opt, self).__init__(**kw)
        # LOCAL_IMPORTS
        from STACK_PY.file_stack_man import File_man
        self.FM             = File_man()

        ## STACK IMPORTS
        from STACK_PY.get_stack import Get_Stack
        self.GS             = Get_Stack()
        #from STACK_PY.build_stack import Build_Stack
        #self.BS             = Build_Stack()
        

        # FLAGS
        self.verbosity      = False
        self.pre_fix        = '+27'
        self.init_seg       = '72'
        self.file_name      = "DEFAULT.txt"
        self.save_stack     = False

        # COLLECTION
        self.current_stack  = []
        self.get_build      = ""
        self.geo_count      = 0

        # ISP_N
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


    # DISPLAY_GOTTEN
    def print_stack(self, level_):
        try:
            if "0" in level_:
                for num in self.current_stack:
                    print("[C_S]:", str(num))
            if "1" in level_:
                for stack in self.current_stack:
                    for num in stack:
                        print("[C_S]:", str(num))
        except Exception as e:
            print(f"[E]:[PRINT_STACK]:[STACK_OPT]:[>{str(e)}<]")




    # PROMPT FOR B_G OPTION(S)
    def get_opts(self, opt_, min_, max_, pre_, init_, save_, verbose_):
        try:
            sure        = ""
            stack_      = []

            # PREFIX
            if pre_:
                self.pre_fix = str(pre_)
            # INIT_SEG (NSP)
            if str(init_) in self.init_segs:
                self.init_seg = str(init_)
            # FILE_TO SAVE TO
            if str(save_):
                self.file_name = str(save_)
                self.save_stack = True
            # VERBOSITY
            if "True" in str(verbose_) :
                self.verbosity = True


            if opt_:
                if "B" in self.get_build.upper():
                    try:
                        print(f"\
                        <--------------------------->\n\
                        [BUILD_STACK_WITH]\n\
                            >>[PRE_]:[{str(pre_)}]\n\
                            >>[INIT_]:[{str(init_)}]\n\
                            >>[MIN_]:[{str(min_)}]\n\
                            >>[MAX_]:[{str(max_)}]\n\
                            >>[SAVE_]:[{str(save_)}]\n\
                            >>[VERBOSE_]:[{str(verbose_)}]\n\
                        <------------------------------->\n")
                        self.BS.main_(pre_, init_, min_, max_, save_, verbose_)
                    except Exception as bs:
                        print(f"[E]:[RUN_STACK_OPT]:[>{str(bs)}<]")

                if "G" in self.get_build.upper():
                    try:
                        print(f"<--------------------------->\n\
                        [GET_STACK_WITH]\
                            >>[PRE_]:[{str(pre_)}]\n\
                            >>[INIT_]:[{str(init_)}]\n\
                            >>[MIN_]:[{str(min_)}]\n\
                            >>[MAX_]:[{str(max_)}]\n\
                            >>[SAVE_]:[{str(save_)}]\n\
                            >>[VERBOSE_]:[{str(verbose_)}]\n\
                        <------------------------------->\n")
                        self.current_stack = self.GS.main_(pre_, init_, min_, max_, save_, verbose_)
                        print(f"[CURRENT_STACK_COUNT]:[>{str(len(self.current_stack))}<]")

                    except Exception as bs:
                        print(f"[E]:[RUN_STACK_OPT]:[>{str(bs)}<]")
            return stack_

        except Exception as e:
            print(f"[E]:[GET_OPTS]:[STACK_OPT]:[>{str(e)}<]")


    # BUILD/GET/QUIT
    def main(self, data):
        opt_    = ""
        param_  = ""
        save_   = ""
        pre_    = ""
        init_   = ""
        verbose_= ""

        GB_     = []
        CNT_    = []
        NSP_    = []
        PR_     = []
        min_    = ""
        max_    = ""

        ret_stack_  = []


        st_data = data.split("*")
        for st_ in st_data:
            print(f"[ST_]:[>{str(st_)}<]")
            if "GB" in str(st_):
                GB_ = st_.split(":")
                opt_ = str(GB_[1])

            if "COUNT" in str(st_):
                CNT_ = st_.split(":")
                pre_ = str(CNT_[1])

            if "ISP" in str(st_):
                NSP_ = st_.split(":")
                init_ = str(NSP_[1])

            if "PARAM" in str(st_):
                PR_ = st_.split("&")
                min_ = str(PR_[0]).replace("PARAMS:", "")
                max_ = str(PR_[1])

        print(">>>[GB_]:",str(opt_))
        print(f">>>[PRE_]:[{pre_}]")
        print(f">>>[NSP_]:[{init_}]")
        print(f">>>[MIN]:[{str(min_)}]")
        print(f">>>[MAX]:[{str(max_)}]")

        try:
            # COLLECT BUILD STACK
            if "G" in opt_:
                self.get_build = "G"
                ret_stack_ = self.get_opts(opt_, min_, max_, pre_, init_, save_, False)

            # BUILD NEW STACK
            if "B" in opt_:
                self.get_build = "B"

            ret_stack =  self.get_opts(opt_, min_, max_, pre_, init_, save_, False)
            return ret_stack

        except Exception as e:
            print(f"[E]:[MAIN]:[STACK_OPT]:[>{str(e)}<]")




#if __name__=="__main__":
#    SOPT = Stack_Opt()
#    SOPT.main()



# to_find_ = f"LEADS*GB:{gb}*COUNT:{cug}*PARAMS:{min_}&{max_}*FILE:{file_}*COUNTRY:{cnt}*ISP:{init_}*VERBOSE:FALSE*"




# LEADS*GB:G*COUNT:NONE*PARAMS:100&200*FILE:NONE*COUNTRY:+27*ISP:72*VERBOSE:FALSE**




