import phonenumbers
from phonenumbers import carrier, geocoder, timezone

import pycountry
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from opencage.geocoder import OpenCageGeocode


import os

class Geo_Stat():
    def __init__(self, **kw):
        super(Geo_Stat, self).__init__(**kw)


    def check_number(self, number):
        try:
            #try:
            #    mobi_valid = phonenumbers.is_valid_number(number)
            #    if mobi_valid != True:
            #        print("[NOT_VALID]:",str(mobi_valid), "\n[NUM]:",str(number))
            #except Exception as v:
            #    print("[E]:[V]:",str(v))

            try:
                mobilo = phonenumbers.parse(number)
                print("[MOBILO]:",str(mobilo))
            except Exception as p:
                print("[E]:[P]:",str(p))
            try:
                mobil_name = carrier.name_for_number(mobilo, 'en')
                print("[MOBI_NAME]:",str(mobil_name))
            except Exception as n:
                print("[E]:[N]:",str(n))
            try:
                mobil_geo = geocoder.description_for_number(mobilo, 'en')
                print("[MOBI_GEO]:",str(mobil_geo))
            except Exception as d:
                print("[E]:[D]:",str(d))
            #try:
            #    return self.get_num_data(number)
            #except Exception as geo:
            #    print("[E]:[GEO]:",str(geo))


        except Exception as e:
            print(f"[E]:[check_number]:[>{str(e)}<]")


    def get_num_data(self, number):
        print(f"[SCAN]:[{str(number)}]")
        try:
            pn = phonenumbers.parse(number) 
            country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
            location = country.name
            print("[_local]:", location)
            try:
                print(carrier.name_for_number(phonenumbers.parse(number), "en"))
            except Exception as c:
                print("[E]:[CARRIER]:",str(c))
            try:
                key = "9c154db12793419092fd6ccb0a77b2a5"
                geocoder = OpenCageGeocode(key)
                query = str(location)
                results = geocoder.geocode(query)
            except Exception as c:
                print("[E]:[OPEN_CAGE]:",str(c))

            #print("[LOCATION]:", str(str(results)[-40:-2]))
            File_man().write_file("STAT/myNum.txt", results, "\n", "w")
            return results
        except Exception as po:
            print("[E]:[GET_STAT]:",str(po))



