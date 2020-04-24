# -*- coding: utf-8 -*-
# author: itimor

import MySQLdb


class MYSQL:
    def __init__(self, db, sql):
        self.sql = sql
        self.conn = MySQLdb.connect(
            host=db["host"],
            port=db["port"],
            user=db["user"],
            passwd=db["passwd"],
            db=db["db"],
            charset='utf8')
        self.cursor = self.conn.cursor()

    def insert(self):
        self.cursor.execute(self.sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return True

    def select(self):
        self.cursor.execute(self.sql)
        alldata = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return alldata

    def update(self):
        self.cursor.execute(self.sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return True


if __name__ == '__main__':
    xxljob_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "TY%pwd123",
        "db": "xxl_job",
    }
    jobapi = MYSQL(xxljob_info)
    sql = "select * from xxl_job_group"
    data = jobapi.insert(sql)
    rep_data = []
    for item in data:
        json_data = {
            "id": item[0],
            "app_name": item[1],
            "title": item[2],
            "order": item[3],
            "address_type": item[4],
            "address_list": item[5],
        }
        rep_data.append(json_data)
    print(rep_data)
