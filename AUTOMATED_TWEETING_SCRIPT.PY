import tweepy
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time


# Your API keys and tokens
API_KEY = ""
API_SECRET_KEY = ""
BEARER_TOKEN = r""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""



# Your tweepy setup
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

post_contents = []



# A function to scrape content from The hackers news website
"""
    Scrapes the website for blog post content.

    Returns:
        list: List of dictionaries containing blog post information.
"""
def scrape_website():
    response = requests.get("https://thehackernews.com/")
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.find_all("div", class_="body-post")
    today = date.today().strftime("%b %d, %Y")

    for article in articles:
        post_date = article.find("div", class_="item-label").text.strip()
        if str(today) in post_date:
            title = article.find("h2", class_="home-title").text.strip()
            url = article.find("a")["href"]
            body = article.find("div", class_="home-desc").text.strip()
            post_content = {"title": title, "url": url, "body": body}
            post_contents.append(post_content)
    return post_contents



"""
    A function to Posts a blog post on Twitter and removes it from the list.

    Args:
        post (dict): Dictionary containing blog post information.
        remaining_time (int): Remaining time until the next post.

    Returns:
        None
"""
def post_to_twitter(post):
    tweet = f"{post['title']}\n\n{post['url']}"
    client.create_tweet(text=tweet)
    print("Successfully posted a blog post on Twitter.")
    post_contents.remove(post)
 
 
    
"""
    Main function to run the Twitter bot.

    Returns:
        None
"""
def main():
    post_interval = 180  # Post every hour (in seconds)
    rescape_interval = 60 * 60 * 6  # Rescrape every 6 hours (in seconds)
    end_time = datetime.now().replace(hour=23, minute=59, second=59)

    while datetime.now() < end_time:
        post_contents = scrape_website()
        while post_contents:
            post = post_contents[0]
            post_to_twitter(post)
            time.sleep(post_interval)

        time.sleep(rescape_interval)

if __name__ == "__main__":
    main()
