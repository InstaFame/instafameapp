#!/usr/bin/python
import praw

reddit = praw.Reddit(client_id='LOeda70Z33ctEA',
    client_secret='C3W-YID8rbZaDhlfIJQPgIbKcys',
    redirect_uri='https://github.com/InstaFame/instafameapp',
    user_agent='testscript by /u/fakebot3')

print(reddit.auth.scopes())
