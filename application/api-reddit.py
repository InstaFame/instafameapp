#!/usr/bin/python
import praw
import os

# Setup Authentication Credentials
def init():
    global reddit
    reddit = praw.Reddit(client_id='LOeda70Z33ctEA',
        client_secret='C3W-YID8rbZaDhlfIJQPgIbKcys',
        redirect_uri='https://github.com/InstaFame/instafameapp',
        user_agent='testscript by /u/instfameapp')

    # Enable read only mode
    reddit.read_only = True

def buildPostsList():
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
           posts_replied_to = f.read()
           posts_replied_to = posts_replied_to.split("\n")
           posts_replied_to = list(filter(None, posts_replied_to))

    return posts_replied_to



def getTopPosts(subInput):
    posts_replied_to = buildPostsList()

    subreddit = reddit.subreddit(subInput)

    for submission in subreddit.hot(limit=5):
        if submission.id not in posts_replied_to :
            print(submission.mod.sticky())

init()
getTopPosts('aww')
