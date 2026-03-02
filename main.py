import asyncio
import csv
import time
from pyrogram import Client
from pyrogram.errors import (
    FloodWait,
    PeerIdInvalid,
    UsernameInvalid,
    UserPrivacyRestricted,
    UserNotMutualContact,
    ChatAdminRequired
)

# Your API credentials
api_id = 1223456  # Your API ID
api_hash = "12113216541141afafafaw"  # Your API hash
phone_number = "+11111111"  # Your phone number with country code

# Configuration
group_username = "just_the_username"  # Target group username
csv_file = "usernames.csv"  # CSV file containing usernames

# Rate limiting settings
ADD_DELAY = 10  # Seconds between additions (adjust based on limits)
BATCH_SIZE = 6  # Users per batch
BATCH_DELAY = 60  # Seconds between batches (5 minutes)

class TelegramMemberAdder:
    def __init__(self):
        self.client = Client(
            "member_adder_session",
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number
        )
        self.added_count = 0
        self.failed_count = 0
        self.skipped_count = 0

    async def start(self):
        """Start the client and begin adding members"""
        try:
            await self.client.start()
            print("✅ Successfully connected to Telegram")
            
            # Get target group
            try:
                self.group = await self.client.get_chat(group_username)
                print(f"✅ Found target group: {self.group.title}")
            except Exception as e:
                print(f"❌ Error accessing group: {e}")
                return
            
            # Check if user is admin
            try:
                await self.client.get_chat_member(self.group.id, "me")
                print("✅ Admin access confirmed")
            except ChatAdminRequired:
                print("❌ You need admin privileges to add members")
                return
            
            # Read usernames from CSV
            usernames = self.read_usernames_from_csv()
            if not usernames:
                print("❌ No usernames found in CSV file")
                return
            
            print(f"📋 Loaded {len(usernames)} usernames from CSV")
            
            # Start adding members
            await self.add_members_batch(usernames)
            
        except Exception as e:
            print(f"❌ Error during execution: {e}")
        finally:
            await self.client.stop()

    def read_usernames_from_csv(self):
        """Read usernames from CSV file"""
        usernames = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].strip():
                        username = row[0].strip().replace('@', '')  # Remove @ if present
                        usernames.append(username)
            return usernames
        except FileNotFoundError:
            print(f"❌ CSV file '{csv_file}' not found")
            return []
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
            return []

    async def add_members_batch(self, usernames):
        """Add members in batches with rate limiting"""
        total_users = len(usernames)
        
        for i in range(0, total_users, BATCH_SIZE):
            batch = usernames[i:i + BATCH_SIZE]
            batch_num = (i // BATCH_SIZE) + 1
            total_batches = (total_users - 1) // BATCH_SIZE + 1
            
            print(f"\n🔄 Processing batch {batch_num}/{total_batches}")
            
            for username in batch:
                await self.add_single_user(username)
            
            # Wait between batches (except for the last batch)
            if i + BATCH_SIZE < total_users:
                print(f"⏳ Waiting {BATCH_DELAY} seconds before next batch...")
                await asyncio.sleep(BATCH_DELAY)
        
        # Final statistics
        print(f"\n📊 Operation Complete:")
        print(f"✅ Successfully added: {self.added_count}")
        print(f"❌ Failed to add: {self.failed_count}")
        print(f"⏭️ Skipped: {self.skipped_count}")

    async def add_single_user(self, username):
        """Add a single user to the group"""
        try:
            # Get user entity
            try:
                user = await self.client.get_users(username)
            except (UsernameInvalid, PeerIdInvalid):
                print(f"❌ User '{username}' not found or invalid")
                self.failed_count += 1
                return
            
            # Add user to group
            try:
                await self.client.add_chat_members(
                    chat_id=self.group.id,
                    user_ids=user.id
                )
                print(f"✅ Added: @{username}")
                self.added_count += 1
                
            except UserPrivacyRestricted:
                print(f"⏭️ Skipped @{username} (privacy settings restrict addition)")
                self.skipped_count += 1
            except UserNotMutualContact:
                print(f"⏭️ Skipped @{username} (not in contacts)")
                self.skipped_count += 1
            except ChatAdminRequired:
                print("❌ Admin privileges required to add members")
                return
            except FloodWait as e:
                print(f"⚠️ Flood wait: {e.value} seconds")
                await asyncio.sleep(e.value)
                # Retry after flood wait
                await self.add_single_user(username)
            except Exception as e:
                print(f"❌ Failed to add @{username}: {str(e)}")
                self.failed_count += 1
            
            # Rate limiting between additions
            await asyncio.sleep(ADD_DELAY)
            
        except Exception as e:
            print(f"❌ Unexpected error with @{username}: {str(e)}")
            self.failed_count += 1

async def main():
    adder = TelegramMemberAdder()
    await adder.start()

if __name__ == "__main__":
    asyncio.run(main())
