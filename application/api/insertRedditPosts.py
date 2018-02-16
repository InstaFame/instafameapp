#!/usr/bin/python

import getRedditPosts
import psycopg2


if __name__ == '__main__':
    getRedditPosts.init
    print getRedditPosts.buildTopPosts('aww')
