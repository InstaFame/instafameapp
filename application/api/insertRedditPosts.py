#!/usr/bin/python

import getRedditPosts
import psycopg2

def connectToDB():
    global cur
    # Connect to database
    conn = psycopg2.connect(dbname="instafame", user="instafame", password="", port=5432)

    # Create connection cursor
    cur = conn.cursor()

def insertStaging(subreddit):

    try:
        cur.execute("SELECT version()")
        rows = cur.fetchall()
        print rows
    except psycopg2.Error as e:
        print "Could not fetch database version. Error: " + str(e.pgerror)

    dict_data = getRedditPosts.main(subreddit)

    # Loop through list for individual dictionaries
    for i in dict_data:
        # Insert each dict as a row
        ql = "INSERT INTO stg." + str(subreddit) + " (" + ", ".join(i.keys()) + ") VALUES (" + ", ".join(["%("+k+")s" for k in i]) + ");"
        cur.execute(sql, dict_data)





if __name__ == '__main__':
    connectToDB()
    insertStaging('aww')
