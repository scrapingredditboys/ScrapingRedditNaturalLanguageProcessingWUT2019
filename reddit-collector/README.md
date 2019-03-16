# Reddit Collector

### Usage:
`collector.py [subreddits...]`

### Description

This script takes the top 1000 posts of all time and extracts all comments if there are at most `LIMIT` of them. Otherwise, it just extracts the submission post. The process terminates when all topics have been extracted or the total number of comments exceed `COMMENTS`.

The results are stored in a PostgreSQL database with tables as defined in `tables.sql` in a database called `reddit`.

In order for the script to work, the `client_id` and `client_secret` need to be replaced with your own credentials as well as your custom `user_agent` string.