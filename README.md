# telegram-member-adder-2026
Finally a bot the works.... 80% of the times :) 


1. Step one

Open CMD and type: pip install -r requirements.txt

2. Step 2

Open main.py and complete this:

api_id = 111111  # Your API ID
api_hash = "abc123ababababab234142"  # Your API hash
phone_number = "+11111111"  # Your phone number with country code

# Configuration
group_username = "just_the_username"  # Target group username
csv_file = "usernames.csv"  # CSV file containing usernames


3. Step 3

Create a file named usernames.csv and upload the files

@username1
@username2
@username3

3.1 Step 3.1

Create a new file named: add_progress.json

There you will find the log of the bot. 

4. Step 4

Open CMD: run python main.py 

If you get the error: ❌ Failed to add @username1: Telegram says: [400 PEER_FLOOD] - The method can't be used because your account is currently limited (caused by "channels.InviteToChannel") - EDIT THIS

ORIGINAL: 
ADD_DELAY = 10  # Seconds between additions (adjust based on limits)
BATCH_SIZE = 6  # Users per batch
BATCH_DELAY = 60  # Seconds between batches (1 minute)

NEW:

ADD_DELAY = 100  # Seconds between additions (adjust based on limits)
BATCH_SIZE = 6  # Users per batch
BATCH_DELAY = 300  # Seconds between batches (5 minutes)

