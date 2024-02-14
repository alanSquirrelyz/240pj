import praw
import datetime
import json
import csv
# import pandas as pd
import praw
from praw.models import MoreComments

# Reddit API credentials
client_id = '1UR5N-Pbu94LG4uZhyVVzg'
client_secret = '9eIspCWr5thf9unovi3S4kQkIu4IWg'
user_agent = 'squirrelhunter'

# Initialize PRAW
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

start_date = datetime.datetime(2022, 1, 1).timestamp()
end_date = datetime.datetime(2023, 12, 31).timestamp()

# Crawl posts, comments, and user information
def crawl_data():
    subreddit = reddit.subreddit('ucr')
    posts = subreddit.new(limit=None)

    with open('reddit_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Post Title', 'Post Date', 'Author', 'Commenter', 'Comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for post in posts:
            if post.created_utc >= start_date and post.created_utc <= end_date:
                author = post.author.name if post.author else '[deleted]'
                writer.writerow({'Post Title': post.title, 'Post Date': datetime.datetime.fromtimestamp(post.created_utc), 'Author': author})

                post.comments.replace_more(limit=None)
                for comment in post.comments.list():
                    commenter = comment.author.name if comment.author else '[deleted]'
                    writer.writerow({'Post Title': post.title, 'Post Date': datetime.datetime.fromtimestamp(post.created_utc), 'Author': author, 'Commenter': commenter, 'Comment': comment.body})

# Main function
def main():
    crawl_data()

if __name__ == "__main__":
    main()
