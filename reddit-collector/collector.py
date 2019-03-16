import praw
import psycopg2
import sys
import datetime

reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='user_agent')

LIMIT = 2000
COMMENTS = 100000
FORMAT_SIZE = len(str(COMMENTS))

con = psycopg2.connect(host = 'localhost',
                       database = 'reddit',
                       user = 'postgres',
                       password = '')
                       
cur = con.cursor()

subreddits = sys.argv[1:]

def getSubmission(s):
  id = s.id
  author_name = getattr(s.author, 'name', None)
  created_utc = datetime.datetime.utcfromtimestamp(s.created_utc).strftime('%Y-%m-%d %H:%M:%S')
  num_comments = s.num_comments
  score = s.score
  selftext = getattr(s, 'selftext', None)
  subreddit_id = s.subreddit_id[3:]
  title = getattr(s, 'title', None)
  upvote_ratio = getattr(s, 'upvote_ratio', None)
  
  return (id, author_name, created_utc, num_comments, score, selftext, subreddit_id, title, upvote_ratio, None, None, False)
  
def getComment(c):
  id = c.id
  author_name = getattr(c.author, 'name', None)
  body = getattr(c, 'body', None)
  created_utc = datetime.datetime.utcfromtimestamp(c.created_utc).strftime('%Y-%m-%d %H:%M:%S')
  score = c.score
  parent_id = c.parent_id[3:]
  submission_id = c.submission.id
  
  return (id, author_name, body, created_utc, score, parent_id, submission_id, None)

for subreddit in subreddits:
  print('Extracting ' + subreddit)
  submission_count = 0
  comment_count = 0
  sub = reddit.subreddit(subreddit)
  cur.execute("INSERT INTO subreddits (id, display_name) VALUES(%s, %s)", (sub.id, sub.display_name))
  con.commit()
  for submission in sub.top('all', limit=None):
    submission_count += 1
    print('  [' + ('{:' + str(FORMAT_SIZE) + '}').format(comment_count) + '/' + str(COMMENTS) + ']' + ' Starting topic ' + str(submission_count))
    
    cur.execute("""INSERT INTO submissions 
                   (id, author_name, created_utc, num_comments, score, selftext, subreddit_id, title, upvote_ratio, selftextner, titlener, isdelisted) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", getSubmission(submission))
    con.commit()

    submission_comments = submission.num_comments
    if submission_comments > LIMIT:
      print('    Topic invalid. Too many comments (' + str(submission_comments) + ')')
      continue
    
    submission.comments.replace_more(limit=None)
    comment_list = submission.comments.list()
    comments = []
    print('    Found ' + str(len(comment_list)) + ' comments.')
    sys.stdout.flush()
    for comment in comment_list:
      comment_count += 1
      comments.append(getComment(comment))
    args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", c) for c in comments)
    cur.execute(b"INSERT INTO comments (id, author_name, body, created_utc, score, parent_id, submission_id, bodyner) VALUES " + args_str)
    con.commit()
    if comment_count >= COMMENTS:
      break
  print('  [' + ('{:' + str(FORMAT_SIZE) + '}').format(comment_count) + '/' + str(COMMENTS) + ']' + ' Finished ' + subreddit)

cur.close()
con.close()