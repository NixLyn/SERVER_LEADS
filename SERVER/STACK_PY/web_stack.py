# BASE 
import os
import re
import threading

# SCRAPER_UTILS
import requests
import html
from bs4 import BeautifulSoup, SoupStrainer
from urlextract import URLExtract
    
# LOCAL
from STACK_PY import file_stack_man 


class Web_Stack():
    def __init__(self, **kw):
        super(Web_Stack, self).__init__(**kw)
        # LOCAL IMPORTS
        from STACK_PY.file_stack_man import File_man
        self.FM = File_man()

        # BASE FLAGS
        self.find = False
        self.save_found = False
        self.verbose = False

        # COMMANDS 
        self.cmd_stack = []
        self.finder = []
        self.flags = []
        self.search = []

        # URL_ DATA
        self.google_ = "https://www.google.com/search?q="
        self.firefox_ = 'https://www.google.com/search?client=firefox-b-e&q='
        self.c_urls_ = []

        # PROFILE DATA
        self.profile_data = []


    # ToDo -> filter and save data
    def extract_profile(self, data_str):
        print("[WEB_RETURN]", data_str)


    # FETCH LINKS FOR: [WITH EXTENSIONS]
    def get_stack_of(self, soup):
        try:
            c_urls_ = []
            hrefs = soup.split('href="/url?q=')
            for i, h in enumerate(hrefs):
                if "http" in h:
                    c_urls_.append(str(h.split("&")[0]))
            return self.filter_urls(c_urls_)
        except Exception as e:
            print(f"[E]:[GET_STACK_OF]:[>{str(e)}<]")


    # FILTER 
    #    [REMOVE_NUANCE]
    def filter_urls(self, url_list):
        try:
            ret_list = []
            for url_ in url_list:
                if "google" not in str(url_) and "body jsmodel" not in str(url_):
                    #print(f"[FILTERED_ULR]:[{str(url_)}]")
                    ret_list.append(url_)
            return ret_list
        except Exception as e:
            print(f"[E]:[FILETER_URLS_]:[{str(e)}]")


    # USES [GOOGLE]:[FIREFOX]:
    #   SCRAPES PAGE -> for links
    def scrape_url(self, pre_url):
        stack_scraped    = ""
        filtered_ = []
        try:
            try:
                print("[TO_FIND]:", pre_url)
                r = requests.get(
                                pre_url,
                                headers={
                                    'Cache-Control': 'no-cache'
                                    }
                                )
                print("[SCRAPE]:[RESPONSE]:", str(r))
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                stack_scraped = self.get_stack_of(str(soup.body))
                #self.FM.write_file("SCRAPED.html", str(soup.body), "\n", "w")
            except Exception as e:
                print(f"[NOPE]:[>{str(e)}<]")

            if stack_scraped:
                for c in stack_scraped:
                    print("[Stack_URLs]:", str(c))

            filtered_ = self.filter_urls(stack_scraped)
            return filtered_ 
        except Exception as c:
            print(f"[E]:[SEARCH_IT]:[>{str(c)}<]")



    # [GOOGLE_DORK]:[FACE_BOOK]
    def fb_dork_(self, number_):
        try:
            try:
                to_dork = number_.replace("+27", "")
            except Exception as e:
                print("[\n>>[reraaag???:[",str(e),"]]<<\n<<<<]")
            to_dork = number_.replace("+27", "")
            fb_dork = f"https://www.google.com/search?q=site%3Afacebook.com+intext%3A%2227{to_dork}%22+OR+intext%3A%22%2B27{to_dork}%22+OR+intext%3A%220{to_dork}%22 "
            r = requests.get(fb_dork)
            print("[FB_DORK]:[RESPONSE]:", str(r))
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            url_list = self.get_stack_of(str(soup.body))
            if len(url_list) == 0:
                return ["FB_DORK", "NOT_FOUND"]
            else:
                return url_list
        except Exception as c:
            print(f"[E]:[FB_DORK]:[>{str(c)}<]")

    # [GOOGLE_DORK]:[TWITTER]
    def tw_dork_(self, number_):
        try:
            try:
                to_dork = number_.replace("+27", "")
                tw_dork = f"https://www.google.com/search?q=site%3Atwitter.com+intext%3A%2227{to_dork}%22+OR+intext%3A%22%2B27{to_dork}%22+OR+intext%3A%220{to_dork}%22  "
                r = requests.get(tw_dork)
                print("[TW_DORK]:[RESPONSE]:", str(r))
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                url_list = self.get_stack_of(str(soup.body))
                if len(url_list) == 0:
                    print("[NO_TW_FOOT_PRINT]")
                    return ["TW_DORK", "NOT_FOUND"]
                else:
                    return url_list

            except Exception as e:
                print("[NO_DORK]", str(e))
        except Exception as c:
            print(f"[E]:[TW_DORK_IT]:[>{str(c)}<]")

    # [GOOGLE_DORK]:[LINKEDIN]
    def li_dork_(self, number_):
        try:
            try:
                to_dork = number_.replace("+27", "")
                li_dork = f"https://www.google.com/search?q=site%3Alinkedin.com+intext%3A%2227{to_dork}%22+OR+intext%3A%22%2B27{to_dork}%22+OR+intext%3A%220{to_dork}%22       "
                r = requests.get(li_dork)
                print("[LI_DORK]:[RESPONSE]:", str(r))
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                url_list = self.get_stack_of(str(soup.body))
                if len(url_list) == 0:
                    print("[NO_LI_FOOT_PRINT]")
                    return ["LI_DORK", "NOT_FOUND"]
                else:
                    return url_list
            except Exception as e:
                print("[NO_DORK]", str(e))
        except Exception as c:
            print(f"[E]:[LI_DORK_IT]:[>{str(c)}<]")

    # [GOOGLE_DORK]:[INSTAGRAM]
    def in_dork_(self, number_):
        try:
            try:
                to_dork = number_.replace("+27", "")
                in_dork = f"https://www.google.com/search?q=site%3Ainstagram.com+intext%3A%2227{to_dork}%22+OR+intext%3A%22%2B27{to_dork}%22+OR+intext%3A%220{to_dork}%22  "
                r = requests.get(in_dork)
                print("[IN_DORK]:[RESPONSE]:", str(r))
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                url_list = self.get_stack_of(str(soup.body))
                if len(url_list) == 0:
                    print("[NO_IN_FOOT_PRINT]")
                    return ["IN_DORK", "NOT_FOUND"]
                else:
                    return url_list
            except Exception as e:
                print("[NO_DORK]", str(e))
        except Exception as c:
            print(f"[E]:[IN_DORK_IT]:[>{str(c)}<]")








# https://www.google.com/search?client=firefox-b-e&q=
# https://www.facebook.com/search/people/?q=helderkruin







