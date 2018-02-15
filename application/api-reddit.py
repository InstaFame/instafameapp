#!/usr/bin/python
import praw
import os

# Setup Authentication Credentials
def init():
    global reddit

    # Define login credentials
    reddit = praw.Reddit(client_id='LOeda70Z33ctEA',
        client_secret='C3W-YID8rbZaDhlfIJQPgIbKcys',
        redirect_uri='https://github.com/InstaFame/instafameapp',
        user_agent='testscript by /u/instfameapp')

    # Enable read only mode
    reddit.read_only = True

# This builds the posted already list. This should accept a subreddit name which with do a DB call against that table
def buildPostsList():
    # Build already posted list if not exists. This needs to be changed to a DB call with each subreddit being it's own table
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
           posts_replied_to = f.read()
           posts_replied_to = posts_replied_to.split("\n")
           posts_replied_to = list(filter(None, posts_replied_to))

    return posts_replied_to

# Function to get the top posts
def getTopPosts(subInput):
    # Get list of already posted posts
    posts_replied_to = buildPostsList()

    # Declare the subreddit to be searched
    subreddit = reddit.subreddit(subInput)

    # Loop through the top 5 hottest current posts
    for submission in subreddit.hot(limit=5):

        # Check if post has already been made, also make sure you're not looking at a stickied thread
        if submission.id not in posts_replied_to and submission.stickied == False :
            print(submission.title)

init()
getTopPosts('aww')
