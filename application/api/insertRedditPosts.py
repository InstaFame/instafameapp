#!/usr/bin/python

import getRedditPosts
import psycopg2




if __name__ == '__main__':
    dict_data = getRedditPosts.main('aww')
    for i in dict_data:
        ql = "INSERT INTO table (" + ", ".join(i.keys()) + ") VALUES (" + ", ".join(["%("+k+")s" for k in i]) + ");"
        print ql
