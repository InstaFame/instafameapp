#!/usr/bin/python

def createStg(subreddit):
    sql = 'CREATE TABLE stg.' + str(subreddit) + '''
    (
        title text COLLATE pg_catalog."default",
        subreddit text COLLATE pg_catalog."default",
        link_id text  COLLATE pg_catalog."default",
        is_video text COLLATE pg_catalog."default",
        score text COLLATE pg_catalog."default",
        shortlink text COLLATE pg_catalog."default",
        is_spoiler text COLLATE pg_catalog."default",
        thumbnail_height text COLLATE pg_catalog."default",
        thumbnail_width text COLLATE pg_catalog."default",
        url text COLLATE pg_catalog."default",
        url_parent text COLLATE pg_catalog."default",
        domain_name text COLLATE pg_catalog."default",
        created_utc text COLLATE pg_catalog."default"
    )'''
    return sql

def truncateStg(subreddit):
    sql = 'TRUNCATE stg.' + str(subreddit) + ';'
    return sql

def upsert(subreddit):
    sql = 'INSERT INTO stg.' + str(subreddit) + ' SELECT * FROM stg.' + str(subreddit) + ' ON CONFLICT (link_id) DO NOTHING'
    return sql
