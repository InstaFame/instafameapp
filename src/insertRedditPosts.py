#!/usr/bin/python

import getRedditPosts
import sendmail
import psycopg2
import getTime
import os
import argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='InstaFame is an autoposter which grabs top posts from Reddit and reposts them on Instagram pages.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-cfg", help="Specifies configuration file. If an error saying 'no module name .py found', be sure to remove the py extension when specifying the file. This configuration file must live in the same directory as this script", required= True)
    parser.add_argument("-host", help="The host of the master node of Postgres database. If no -host if specified the script will use the PGHOST environment variable if it is set")
    parser.add_argument("-p", help="-port : The port for the master node of the Postgres database. If no -port is specified the script will use the PGPORT environment variable if it is set", type=int)
    parser.add_argument("-db", help="The database being used. If no db is specified the script will use the PGDATABASE environment variable if it is set")
    parser.add_argument("-usr", help="User to log into the database under")
    parser.add_argument("-sub", help="Subreddit to execute script on", required = True)
    parser.add_argument("-test", help="Executes this script as a test script. This means that transactions won't be committed to the database and email alerts will not be sent out.", action='store_true')

    args = parser.parse_args()
    path = os.path.splitext(args.cfg )[0]

    if path:
        cfg = __import__(path)
    else:
        raise argparse.ArgumentTypeError( "You must specify a configuration file using the -cfg command following the Instafame script. Make sure that you don't include the .py extention when specifying it and ensure that the config file is in the same directory as the gpLoad script. For more information, enter 'python gpLoad.py -h into the command line." )

    if args.host:
        cfg.host = args.host
    if args.p:
        cfg.port = args.p
    if args.db:
        cfg.db = args.db
    if args.usr:
        cfg.user = args.usr
    if args.test:
        cfg.test = args.test
    if args.sub:
        cfg.subreddit = args.sub

    return cfg


def connectToDB():
    cfg = parseArguments()
    # Connect to database
    conn = psycopg2.connect(dbname=cfg.db, user=cfg.user, password=cfg.pw, port=cfg.port, host=cfg.host)

    return conn

def insertStaging():

    cfg = parseArguments()

    # Setup Connection to Database
    conn = connectToDB()

    # Create connection cursor
    cur = conn.cursor()

    subreddit = cfg.subreddit

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
        sql = "INSERT INTO stg." + str(subreddit) + " (" + ", ".join(i.keys()) + ") VALUES (" + ", ".join(["%("+k+")s" for k in i]) + ");"
        try:
            execute = cur.execute(sql, i)
            commit = conn.commit()
            successful_rows = successful_rows + 1
        except Exception as e:
            insertError = e
            print insertError
            commit = conn.commit()
            failed_rows = failed_rows + 1

    if failed_rows == 0 and successful_rows != 0:
        subject = "Insert Staging Subreddit: /r/" + str(subreddit) + " - SUCCESS"
        body = "Job inserting staging was successful at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows)
        if cfg.test == True:
            print(subject + '\n' + body)
        else:
            sendmail.sendAlert(subject,body)
    elif failed_rows != 0 and successful_rows != 0:
        subject = "Insert Staging Subreddit: /r/" + str(subreddit) + " - PARTIAL"
        body = "Job inserting staging was successful with errors at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows)
        if cfg.test == True:
            print(subject + '\n' + body)
        else:
            sendmail.sendAlert(subject,body)

    else:
        subject = "Insert Staging Subreddit: /r/" + str(subreddit) + " - FAILED"
        body = "Job inserting staging has failed with all inserts at " + str(getTime.getTimestamp()) + ".\n\nSuccessfully Inserted Rows: " + str(successful_rows) + "\nFailed Inserted Rows: " + str(failed_rows) + "\n\nError message: " + str(insertError)
        if cfg.test == True:
            print(subject + '\n' + body)
        else:
            sendmail.sendAlert(subject,body)

if __name__ == '__main__':
    insertStaging()
