# Reddit Collector

### Usage:
`python collector.py [subreddits...]`

### Description

This script takes the top 1000 posts of all time and extracts all comments if there are at most `LIMIT` of them. Otherwise, it just extracts the submission post. The process terminates when all topics have been extracted or the total number of comments exceed `COMMENTS`. This happens for all subreddits specified in the arguments.

The results are stored in a PostgreSQL database with tables as defined in `tables.sql` in a database called `reddit`.

In order for the script to work, the `client_id` and `client_secret` need to be replaced with your own credentials as well as your custom `user_agent` string.

# Subreddit Validator

### Usage:
`python validator.py [subreddits...]`

### Description

This script outputs which subreddits have at least `COMMENTS` comments after applying the limit of `LIMIT`. Requires similar configuration as stated above.