import pandas as pd
import streamlit as st
from db import Database

DB_FILE = "listed.db"

class ListManager:
    def __init__(self, DB_FILE):
        self.__db = Database(DB_FILE)
        self.__current_whitelist = None
        self.__current_blacklist = None
    
    def manage_lists(self):
        whitelist = st.file_uploader("Whitelist File (CSV)", 
                                  type=["csv"],
                                  accept_multiple_files=False)
        blacklist = st.file_uploader("Blacklist File (CSV)", 
                                    type=["csv"],
                                    accept_multiple_files=False)
        if whitelist and whitelist is not self.__current_whitelist:
            db.replace_whitelist(whitelist)
            self.__current_whitelist = whitelist
            st.success("Whitelist Update Successful")
        elif blacklist and blacklist is not self.__current_blacklist:
            db.replace_blacklist(blacklist)
            self.__current_blacklist = blacklist
            st.success("Blacklist Update Successful")
        elif not self.__current_whitelist and not self.__current_blacklist:
            st.error("No Lists Inputted")
    
    def __sort_matches(self, full_name: list):
        match = self.__db.get_absolute_matches(full_name)
        whitelisters, blacklisters = []
        matches = self.__db.get_matches(full_name)
        for person in matches:
            name = person["firstname"] + " " + person["lastname"]
            if person["status"] == 0:
                blacklisters.append(name.title())
            else:
                whitelisters.append(name.title())
        return (match, whitelisters, blacklisters)
    
    def display_result(self, full_name: list):
        res = self.__sort_matches(full_name)
        if res[0]:
            if res[0][0] == 0:
                st.error("Blacklisted")
            else:
                st.success("Whitelisted")
        elif res[2]:
            st.warning("Possible Blacklist Matches")
            for match in res[2]:
                st.write(match)
        elif res[1]:
            st.warning("Possible Whitelist Matches")
            for match in res[1]:
                st.write(match)
        else:
            st.error("Not Listed")


def setup_streamlit():
    st.set_page_config(layout="wide")
    st.title('Whitelist Assist')
    st.write("Alejandro Alonso UChicago '26")

if __name__ == "__main__":
    db = Database(DB_FILE)
    setup_streamlit()
    whitelists = upload_whitelists()
    raw_w, whitelist, raw_b, blacklist = get_lists(whitelists, B_SHEET)

    st.header("Check Name")
    names = st.text_input("First Name Last Name: ", "Joe Smith").split(" ")
    to_check = list(map(str.lower, db.parse_names(names)))
    
    check_name(to_check, whitelist, blacklist)
    st.text("")
    
    
    

    st.text("")

    #st.header("Full Blacklist")
    #st.table(raw_b)