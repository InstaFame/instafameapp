#!/usr/bin/python

import getRedditPosts
import psycopg2

def connectToDB():
    global cur
    global conn
    # Connect to database
    conn = psycopg2.connect(dbname="instafame", user="instafame", password="", port=5432, host='localhost')

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
        sql = "INSERT INTO stg." + str(subreddit) + " (" + ", ".join(i.keys()) + ") VALUES (" + ", ".join(["%("+k+")s" for k in i]) + ");"
        execute = cur.execute(sql, i)
        commit = conn.commit()
        print commit



if __name__ == '__main__':
    connectToDB()
    insertStaging('aww')
