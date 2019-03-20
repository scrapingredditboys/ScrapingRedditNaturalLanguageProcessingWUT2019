CREATE TABLE Subreddits (
 id varchar(10) PRIMARY KEY,
 display_name varchar(30)
);

CREATE TABLE Submissions (
 id VARCHAR(10) PRIMARY KEY,
 author_name VARCHAR(50),
 created_utc TIMESTAMP,
 num_comments INTEGER,
 score INTEGER,
 selftext VARCHAR(50000),
 subreddit_id VARCHAR(10),
 title VARCHAR(500),
 upvote_ratio NUMERIC(3, 2),
 selftextNER VARCHAR(100000),
 titleNER VARCHAR(1000),
 isDelisted BOOLEAN
);

CREATE TABLE Comments (
 id VARCHAR(10) PRIMARY KEY,
 author_name VARCHAR(50),
 body VARCHAR(50000),
 created_utc TIMESTAMP,
 score INTEGER,
 parent_id VARCHAR(10),
 submission_id VARCHAR(10),
 bodyNER VARCHAR(100000)
);