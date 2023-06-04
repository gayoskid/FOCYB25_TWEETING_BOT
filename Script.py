import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
from Twitter_API_Config import *
import tkinter as tk

"""
    Scrapes the website for blog post content.
    Returns:
        list: List of dictionaries containing blog post information.
"""
post_contents = []
def automated():
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
            elif str(today) not in post_date:
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
 

#gui codes 
def run_gui():
    def tweet():
        try:
            text = text_entry.get()
            client.create_tweet(text=text)
            text_entry.delete(0, tk.END)
            print("Post tweeted successfully!".upper())
        except Exception as error:
            print("Error occured when trying to tweet a post!".upper(), error)

    def retweet():
        try:
            tweet_id = tweet_id_entry.get()
            client.retweet(tweet_id)
            tweet_id_entry.delete(0, tk.END)
        except Exception as error:
            print("An error occured when trying to retweet!".upper(), error)

    # Create the GUI
    window = tk.Tk()
    window.title("Twitter Bot")
    window.geometry("500x300")
    window.config(bg="#283747")

    # Header
    header_label = tk.Label(window, text="Twitter Bot", font=("Arial", 24), fg="#ffffff", bg="#283747")
    header_label.pack(pady=20)

    # Tweet Section
    tweet_frame = tk.Frame(window, bg="#34495e")
    tweet_frame.pack(pady=10)

    tweet_label = tk.Label(tweet_frame, text="Tweet", font=("Arial", 18), fg="#ffffff", bg="#34495e")
    tweet_label.pack(pady=10)

    text_entry = tk.Entry(tweet_frame, font=("Arial", 12), width=40)
    text_entry.pack(pady=5)

    tweet_button = tk.Button(tweet_frame, text="Tweet", font=("Arial", 12), bg="#2ecc71", fg="#ffffff", padx=10, pady=5, command=tweet)
    tweet_button.pack(pady=10)

    # Retweet Section
    retweet_frame = tk.Frame(window, bg="#34495e")
    retweet_frame.pack(pady=10)

    retweet_label = tk.Label(retweet_frame, text="Retweet", font=("Arial", 18), fg="#ffffff", bg="#34495e")
    retweet_label.pack(pady=10)

    tweet_id_entry = tk.Entry(retweet_frame, font=("Arial", 12), width=40)
    tweet_id_entry.pack(pady=5)

    retweet_button = tk.Button(retweet_frame, text="Retweet", font=("Arial", 12), bg="#2ecc71", fg="#ffffff", padx=10, pady=5, command=retweet)
    retweet_button.pack(pady=10)

    # Start the GUI
    window.mainloop()


#check for authentication connection from Twitter_API_Config.py    
Check_auth_conn()


# Ask the user which version to run
while True:
    try:
        choice = input("\nWhich version of the bot do you want to run? \n\nEnter 'AUTOMATED TWEETING' or 'GUI TWEETING': ")
        if choice.lower() == 'gui tweeting':
            run_gui()
            break
        elif choice.lower() == 'automated tweeting':
            automated()
            break
        else:
            print(f"Invalid choice: {choice} \n\nPlease enter 'AUTOMATED_TWEETING' or 'GUI_TWEETING'.")
    except Exception as error:
        print("An error Has occured!", error)