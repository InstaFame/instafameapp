#!/usr/bin/python
import praw
import os
from urlparse import urlparse

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

def parseUrl(submissionLink):
    parsedUrl = urlparse(submissionLink)
    domain = '{uri.netloc}'.format(uri=parsedUrl)

    return domain

def setDomain(domain):
    if domain == 'i.imgur.com':
        domain = 'imgur'
    elif domain == 'gfycat.com':
        domain = 'gfycat'
    elif domain == 'i.redd.it':
        domain = 'reddit'
    else:
        domain = 'unparsed'

    return domain

# Function to get the top posts
def buildTopPosts(subInput):
    global reddit

    # Get list of already posted posts
    posts_replied_to = buildPostsList()

    # Declare the subreddit to be searched
    subreddit = reddit.subreddit(subInput)

    listPost = []

    # Loop through the top 5 hottest current posts
    for submission in subreddit.top('month'):

        # Check if post has already been made, also make sure you're not looking at a stickied thread
        if submission.id not in posts_replied_to and submission.stickied == False :

            # Creates a dictionary of each individual post
            dictPost = {}

            #print("Title: " + submission.title)
            dictPost['title'] = submission.title
            #print("Link ID: " + str(submission.id))
            dictPost['link_id'] = submission.id
            #print("Is Video: " + str(submission.is_video))
            dictPost['is_video'] = submission.is_video
            #print("Score: " + str(submission.score))
            dictPost['score'] = submission.score
            #print("Shortlink: " + str(submission.shortlink))
            dictPost['shortlink'] = submission.shortlink
            #print("Is Spoiler: " + str(submission.spoiler))
            dictPost['is_spoiler'] = submission.spoiler
            #print("Thumbnail Height: " + str(submission.thumbnail_height))
            dictPost['thumbnail_height'] = submission.thumbnail_height
            #print("Thumbnail Width: " + str(submission.thumbnail_width))
            dictPost['thumbnail_width'] = submission.thumbnail_width
            #print("URL: " + str(submission.url))
            dictPost['url'] = submission.url
            #print("URL Parent: " + str(parseUrl(submission.url)))
            dictPost['url_parent'] = parseUrl(submission.url)
            #print("Domain: ") + str(setDomain(parseUrl(submission.url)))
            dictPost['domain_name'] = setDomain(parseUrl(submission.url))

        listPost.append(dictPost.copy())

    return listPost

def main(subreddit):
    init()
    return buildTopPosts(subreddit)

if __name__ == "__main__":
    main()
