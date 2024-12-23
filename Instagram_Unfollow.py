import json
import time
import random
from seleniumbase import SB
from bs4 import BeautifulSoup
import csv 
import datetime
import glob

def random_delay(min_seconds=2, max_seconds=5):
    """Introduce a random delay between actions to mimic human behavior."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Extract usernames
            usernames = []
    
            for entry in data:
                    # Ensure string_list_data exists and is not empty
                if "string_list_data" in entry and entry["string_list_data"]:
                    usernames.append(entry["string_list_data"][0]["value"])
    except Exception as e:
                print(f"Error processing data: {e}")
    return usernames

def load_json_for_following(file_path):
    """
    Loads and parses a JSON file to extract usernames from the `relationships_following` key.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of usernames.
    """
    usernames = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for i in data:
                content = i["string_list_data"]
                name= (content[0])["value"]
                usernames.append(name)  
            return usernames # Return the populated list
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []

def find_people_to_follow(post_urls):
    # Load following data
    following_path = "connections/followers_and_following/following.json"
    following = load_json_for_following(following_path)
    
    # Set to store unique usernames for current run
    unique_usernames = set()
    
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)
        
        # Load cookies from the JSON file
        with open("cookies.json", "r") as file:
            cookies = json.load(file)

        # Add each cookie to the browser
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

        # Process each URL in the list
        for post_url in post_urls:
            try:
                print(f"Processing post: {post_url}")
                sb.open(post_url)
                time.sleep(1)
                
                page_source = sb.get_page_source()
                soup = BeautifulSoup(page_source, 'html.parser')
                elements = soup.find_all(class_="_ap3a _aaco _aacw _aacx _aad7 _aade")
                
                # Process each username from current post
                for element in elements:
                    username = element.get_text()
                    # Only add username if not already in our set and not in following
                    if username not in unique_usernames and username not in following:
                        unique_usernames.add(username)
                        print(f"Added new username: {username}")
                
                print(f"Current unique users count: {len(unique_usernames)}")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing post {post_url}: {e}")
                continue
        
        # Save results to CSV
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"potential_follows_{timestamp}.csv"
        
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Username', 'Source Posts', 'Timestamp'])
                
                for username in unique_usernames:
                    writer.writerow([
                        username,
                        ','.join(post_urls),
                        timestamp
                    ])
                
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
    # First read usernames from CSV
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
    
    # Start browser session
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)
        
        # Load cookies from the JSON file
        try:
            with open("cookies.json", "r") as file:
                cookies = json.load(file)

            # Add each cookie to the browser
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

        # Process each username
        for user in usernames:
            try:
                sb.open(f"https://www.instagram.com/{user}")
                time.sleep(1)
                sb.click('button[class=" _acan _acap _acaq _acas _aj1- _ap30"]', timeout=2, delay=1)
                # random_delay(1, 3)  # Random delay between 1 and 3 seconds
                print(f"Sent request to: {user}")
                sent_requests_to.append(user)
            except Exception as e:
                print(f"Error processing {user}: {e}")
                continue
    return sent_requests_to  

def unfollow_people():
    # Load following data
    following_path = "connections/followers_and_following/following.json"
    followers_path = "connections/followers_and_following/followers_1.json"
    following = load_json_for_following(following_path)
    follower = load_json(followers_path)
    
    people_to_unfollow = []

    for user in following:
        if user not in follower:
            people_to_unfollow.append(user)
    
    # Start browser session
    with SB(browser='chrome') as sb:
        sb.get("https://www.instagram.com")
        time.sleep(3)
        
        # Load cookies from the JSON file
        try:
            with open("cookies.json", "r") as file:
                cookies = json.load(file)

            # Add each cookie to the browser
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

        # Process each username
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

# Run the script
if __name__ == "__main__":
    unfollow_list = unfollow_people()
    print(f"Unfollowed {len(unfollow_list)} users")
    
# https://github.com/brij0/Instagram_unfollow