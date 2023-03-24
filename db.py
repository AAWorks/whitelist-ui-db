import sqlite3
from notanorm import SqliteDb
import pandas as pd
from itertools import chain

''' Database-related Functions '''

class Database:
    def __init__(self, db_file: str):
        self.__db = SqliteDb(db_file)
        # 1: whitelisted, 0: blacklisted
        self.__db.query("CREATE TABLE IF NOT EXISTS people (firstname TEXT, \
                lastname TEXT, status INTEGER, id INTEGER PRIMARY KEY AUTOINCREMENT;") 
        self._db.close()

    def parse_names(self, names):
        return names + ["None"] if len(names) > 2 else [names[0], names[-1]]
    
    def __add_name(self, names: list, status: int):
        names = self.parse_names(names)
        self.__db.insert("people", firstname=names[0], 
                       lastname=names[1], status=status)
    
    def __clear_db(self, status=-1):
        if status == -1:
            self.__db.delete_all("people")
        else:
            self.__db.delete("people", status=status)

    def replace_whitelist(self, sheet):
        raw = pd.read_csv(sheet, sep=",")
        lst = raw.drop(raw.columns[0], axis=1).values.tolist()
        lst = [x.lower() for x in list(chain.from_iterable(lst)) if isinstance(x, str)]
        self.__clear_db(1)
        for name in lst:
            if not self.get_absolute_matches(self, name):
                self.__add_name(name.split(" "), 1)

    def replace_blacklist(self, sheet):
        raw = pd.read_csv(sheet, sep=",")
        lst = [x.lower() for x in raw.Name.values.tolist() if type(x) == str]
        self.__clear_db(0)
        for name in lst:
            matches = self.get_absolute_matches(self, name)
            if matches:
                self.__db.delete("people", id=matches[0]["id"])
            self.__add_name(name.split(" "), 0)

    def get_absolute_matches(self, full_name: list):
        abs_matches = self.__db.select("people", firstname=full_name[0],
                                       lastname=full_name[1])
        return abs_matches
    
    def get_matches(self, full_name: list) -> list[dict]:
        full_name = self.parse_names(full_name)
        first_matches = self.__db.select("people", firstname=full_name[0])
        last_matches = self.__db.select("people", lastname=full_name[1])
        return first_matches + last_matches
