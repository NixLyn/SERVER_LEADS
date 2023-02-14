# ToDo:
    # REPLACE WITH CALLERPY

from truecallerpy import search_phonenumber
import subprocess


class TrueCallerScan():
    def __init__(self, **kw):
        super(TrueCallerScan, self).__init__(**kw)
        self.id_ = subprocess.getoutput('truecallerpy -i')

    # NAME
    def get_name(self, number_):
        try:
            got_name = subprocess.getoutput(f'truecallerpy -s {number_} --name')
            if got_name:
                print(f"[GOT_NAME]:[>{got_name}<]")
                return got_name
        except Exception as e:
            print(f"[E]:[GET_NAME]:[TCS]:[>{str(e)}<]")

    # EMAIL
    def get_email(self, number_):
        try:
            got_email = commands.getoutput(f'truecallerpy -s {number_} --email')
            if got_email:
                print(f"[GOT_EMAIL]:[>{got_email}<]")
                return got_email
        except Exception as e:
            print(f"[E]:[GET_EMAIL]:[TCS]:[>{str(e)}<]")


    # PALL
    def get_pall(self, number_):
        try:
            got_pall = commands.getoutput(f'truecallerpy -s {number_}')
            if got_pall:
                print(f"[GOT_PALL]:[>{got_pall}<]")
                return got_pall
        except Exception as e:
            print(f"[E]:[GET_PALL]:[TCS]:[>{str(e)}<]")

