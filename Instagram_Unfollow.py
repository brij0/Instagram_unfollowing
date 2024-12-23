import json
import time
import random
from seleniumbase import SB
from bs4 import BeautifulSoup
import csv
import datetime

def random_delay(min_seconds=2, max_seconds=5):
    """Introduce a random delay between actions to mimic human behavior."""
    # Sleep for a random amount of time between min_seconds and max_seconds
    time.sleep(random.uniform(min_seconds, max_seconds))

def load_json(file_path):
    """Load JSON data from a file and extract usernames."""
    # Try to open and read the JSON file, extracting usernames from the data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            usernames = [entry["string_list_data"][0]["value"] for entry in data if "string_list_data" in entry and entry["string_list_data"]]
    except Exception as e:
        # Print an error message if something goes wrong
        print(f"Error processing data: {e}")
        return []
    return usernames

def load_json_for_following(file_path):
    """Load JSON data from a file and extract usernames from the `relationships_following` key."""
    # Try to open and read the JSON file, extracting usernames from the data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            usernames = [i["string_list_data"][0]["value"] for i in data]
    except Exception as e:
        # Print an error message if something goes wrong
        print(f"Error loading JSON file {file_path}: {e}")
        return []
    return usernames

def find_people_to_follow(post_urls):
    """Find potential users to follow based on post URLs."""
    # Load the list of users you are already following
    following_path = "connections/followers_and_following/following.json"
    following = load_json_for_following(following_path)
    unique_usernames = set()

    # Use SeleniumBase to interact with Instagram
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)

        # Load cookies to maintain session
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                cookie.pop('sameSite', None)
                cookie.pop('storeId', None)
                cookie.pop('id', None)
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                try:
                    sb.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie: {e}")
                    continue

        # Iterate over each post URL to find potential users to follow
        for post_url in post_urls:
            try:
                sb.open(post_url)
                time.sleep(1)
                page_source = sb.get_page_source()
                soup = BeautifulSoup(page_source, 'html.parser')
                elements = soup.find_all(class_="_ap3a _aaco _aacw _aacx _aad7 _aade")

                # Extract usernames from the page
                for element in elements:
                    username = element.get_text()
                    if username not in unique_usernames and username not in following:
                        unique_usernames.add(username)
                        print(f"Added new username: {username}")

                print(f"Current unique users count: {len(unique_usernames)}")
                time.sleep(1)

            except Exception as e:
                print(f"Error processing post {post_url}: {e}")
                continue

        # Save the results to a CSV file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"potential_follows_{timestamp}.csv"

        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Username', 'Source Posts', 'Timestamp'])
                for username in unique_usernames:
                    writer.writerow([username, ','.join(post_urls), timestamp])

            print(f"Results saved to {csv_filename}")
            print(f"Found {len(unique_usernames)} unique potential users to follow")

            return {
                'potential_follows': list(unique_usernames),
                'csv_file': csv_filename,
                'unique_users_found': len(unique_usernames)
            }

        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return None

    return None

def follow_people(csv_file_path):
    """Follow users listed in a CSV file."""
    # Load usernames from the CSV file
    try:
        usernames = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Username' in row:
                    usernames.append(row['Username'])
    except Exception as e:
        print(f"Error reading CSV file {csv_file_path}: {e}")
        return []

    sent_requests_to = []

    # Use SeleniumBase to interact with Instagram
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)

        # Load cookies to maintain session
        try:
            with open("cookies.json", "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    cookie.pop('sameSite', None)
                    cookie.pop('storeId', None)
                    cookie.pop('id', None)
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        sb.add_cookie(cookie)
                    except Exception as e:
                        print(f"Error adding cookie: {e}")
                        continue
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return []

        # Iterate over each username and send a follow request
        for user in usernames:
            try:
                sb.open(f"https://www.instagram.com/{user}")
                time.sleep(1)
                sb.click('button[class=" _acan _acap _acaq _acas _aj1- _ap30"]', timeout=2, delay=1)
                print(f"Sent request to: {user}")
                sent_requests_to.append(user)
            except Exception as e:
                print(f"Error processing {user}: {e}")
                continue

    return sent_requests_to

def unfollow_people():
    """Unfollow users who do not follow back."""
    # Load the list of users you are following and your followers
    following_path = "connections/followers_and_following/following.json"
    followers_path = "connections/followers_and_following/followers_1.json"
    following = load_json_for_following(following_path)
    followers = load_json(followers_path)

    # Determine which users to unfollow
    people_to_unfollow = [user for user in following if user not in followers]

    # Use SeleniumBase to interact with Instagram
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)

        # Load cookies to maintain session
        try:
            with open("cookies.json", "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    cookie.pop('sameSite', None)
                    cookie.pop('storeId', None)
                    cookie.pop('id', None)
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        sb.add_cookie(cookie)
                    except Exception as e:
                        print(f"Error adding cookie: {e}")
                        continue
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return []

        # Iterate over each user and unfollow them
        for user in people_to_unfollow:
            try:
                sb.open(f"https://www.instagram.com/{user}")
                time.sleep(1)
                sb.click('button[class=" _acan _acap _acat _aj1- _ap30"]', timeout=2, delay=1)
                sb.sleep(0.1)
                unfollow_button = sb.find_element("//span[contains(text(), 'Unfollow')]")
                unfollow_button.click()
                sb.sleep(0.5)
                print(f"Unfollowed: {user}")
            except Exception as e:
                print(f"Error processing {user}: {e}")
                continue

    return people_to_unfollow

if __name__ == "__main__":
    # Unfollow users who do not follow back and print the count of unfollowed users
    unfollow_list = unfollow_people()
    print(f"Unfollowed {len(unfollow_list)} users")
