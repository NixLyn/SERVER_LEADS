import phonenumbers
from phonenumbers import timezone, carrier, geocoder
import subprocess



class NumPho():
    def __init__(self, **kw):
        super(NumPho, self).__init__(**kw)
        pass




    # FILTER _CURL_ 
    def filter_curl(self, curl_ret):
        try:
            heap_ = curl_ret.split("\n")
            for h_ in heap_:
                if "IP " in str(h_):
                    ch_ = str(h_)[17:-5]
                    return str(ch_)
        except Exception as e:
            print(f"[E]:[FILTER_URL]:[{str(e)}]")

    # GET IP VALUE
    def get_ip_(self, number_):
        try:
            ret_list    = []
            to_curl     = f"curl https://wrsa.ru/{number_}"
            curl_ret    = subprocess.getoutput(to_curl)
            c_filter = self.filter_curl(curl_ret)
            print(f"[FILTER_ED]:[{str(c_filter)}]")

            to_geo      = f""
            curl_ret    = subprocess.getoutput(to_curl)



            return c_filter
        except Exception as e:
            print(f"[E]:[GET_IP]:[{str(e)}]")




    # STANDARD DATA
    def check_num_data_(self, number_):
        try:
            ret_list = []
            phone_number = phonenumbers.parse(number_)
            valid_ = phonenumbers.is_valid_number(phone_number)
            ret_list.append(valid_)
            tz_ = timezone.time_zones_for_number(phone_number)
            ret_list.append(tz_)
            nsp_ = geocoder.description_for_number(phone_number, "en")
            ret_list.append(nsp_)


            print(f"[VALID_CHECK]:[{str(valid_)}]")
            print(f"[TZONE_CHECK]:[{str(tz_)}]")
            print(f"[CARIR_CHECK]:[{str(nsp_)}]")

            return valid_
        except Exception as e:
            print(f"[E]:[IS_NUM_VALID]:[{str(e)}]")

    # FILTER_411
    def filter_411(self, curl_ret):
        try:
            heap_ = curl_ret.split("\n")
            for h_ in heap_:
                print("[H-]:",str(h_))
                if "IP " in str(h_):
                    ch_ = str(h_)[17:-5]
                    return str(ch_)
        except Exception as e:
            print(f"[E]:[FILTER_411]:[{str(e)}]")

    # 411 LOOK_UP
    def do_411(self, number_):
        try:
            the_dig_ = f"https://www.411locate.com/reverse-phone/{number_}"

            curl_ret    = subprocess.getoutput(the_dig_)
            print("[CURL_RET]:",str(curl_ret))
            c_filter = self.filter_411(curl_ret)

            print(f"[FILTER_ED]:[{str(c_filter)}]")

            return c_filter
        except Exception as e:
            print(f"[E]:[DO_411]:[{str(e)}]")





