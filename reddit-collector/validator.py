import praw
import sys

reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='user_agent')

LIMIT = 2000
COMMENTS = 100000

subreddits = sys.argv[1:]

print('\nVALIDITY' + '{:^30}'.format('SUBREDDIT') + 'COMMENTS\n')

for subreddit in subreddits:
  sub = reddit.subreddit(subreddit)
  sum = 0
  for submission in sub.top('all', limit=None):
    count = submission.num_comments
    if count <= LIMIT:
      sum += count
  if sum >= COMMENTS:
    print('VALID   ' + '{:30}'.format(subreddit) + ' ' + str(sum))
  else:
    print('INVALID ' + '{:30}'.format(subreddit) + ' ' + str(sum))