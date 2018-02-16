#!/usr/bin/python

import getRedditPosts
import sendmail
import psycopg2
import getTime

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

    failed_rows = 0
    successful_rows = 0
    insertError = ''

    # Loop through list for individual dictionaries
    for i in dict_data:
        # Insert each dict as a row
        print i
        sql = "INSERT INTO stg." + str(subreddit) + " (" + ", ".join(i.keys()) + ") VALUES (" + ", ".join(["%("+k+")s" for k in i]) + ");"
        try:
            execute = cur.execute(sql, i)
            commit = conn.commit()
            successful_rows = successful_rows + 1
        except Exception as e:
            insertError = e
            failed_rows = failed_rows + 1

    if failed_rows == 0:
        sendmail.sendAlert("Insert Staging Subreddit: /r/" + str(subreddit) + " - SUCCESS",
    "Job inserting staging was successful at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows))
    elif failed_rows != 0 and successful_rows != 0:
        sendmail.sendAlert("Insert Staging Subreddit: /r/" + str(subreddit) + " - PARTIAL",
    "Job inserting staging was successful with errors at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows))
    else:
        sendmail.sendAlert("Insert Staging Subreddit: /r/" + str(subreddit) + " - FAILED",
    "Job inserting staging has failed with all inserts at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows) + "\n\nError message: " + str(insertError))

if __name__ == '__main__':
    connectToDB()
    insertStaging('aww')
