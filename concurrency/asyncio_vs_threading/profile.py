# Build an asyncio-based profile aggregation service.
# You have these async APIs available:
# get_user(user_id) -> user
# get_posts(user_id) -> posts
# get_friends(user_id) -> friends
# Assume all three are I/O-bound async functions that may take an unpredictable amount of time. You can simulate them with asyncio.sleep() while testing.
# Given a user_id:
# Fetch the user first.
# Once you have the user's ID, fetch their posts and friends concurrently.
# Once both complete, construct and return:
# {
#     "user": ...,
#     "posts": ...,
#     "friends": ...
# }
# The entire operation must have a 5-second timeout.
# If get_posts() or get_friends() fails, the profile operation should fail rather than returning a partial profile.
# If the operation times out, make sure the underlying work does not continue running in the background.
# Don't create unnecessary tasks.
# Constraints:
# asyncio only.
# No threads.
# No third-party libraries.
# Use asyncio.gather() and/or asyncio.create_task().
# Don't implement the mock APIs yet. Assume they already exist.
# Test these cases:
# Both child operations succeed.
# get_posts() fails.
# get_friends() fails.
# One child operation takes longer than 5 seconds.
# get_user() itself takes longer than 5 seconds.

import asyncio
from dataclasses import dataclass
import string 
import random 
import time

@dataclass
class User:
    user_id: int
    user_name: str

@dataclass 
class Post:
    post_id: int
    content: str 

@dataclass
class UserProfile:
    user: User 
    posts: list[Post]
    friends: list[User]



class ProfileService:
    def __init__(self):
        pass 

    async def get_user(self, user_id, username="Dummy"):
        await asyncio.sleep(1)
        return User(user_id, username)   

    async def get_posts(self, user_id):
        await asyncio.sleep(3)
        posts = []
        for i in range(10):
            posts.append(Post(i, content=f"{''.join(random.choices(string.ascii_letters, k=10))}"))
        return posts

    async def get_friends(self, user_id):
        await asyncio.sleep(2)
        friends = []
        for i in range(10):
            friends.append(User(i, user_name=f"{''.join(random.choices(string.ascii_letters, k=10))}"))
        return friends
        
    async def get_profile(self, user_id):
        async with asyncio.timeout(2):
            try:
                user = await self.get_user(user_id)
            except Exception as E:
                print(E)
                return 
            # friends = asyncio.create_task(self.get_friends(user.user_id))
            # posts = asyncio.create_task(self.get_posts(user.user_id))
            res = await asyncio.gather(self.get_friends(user.user_id), self.get_posts(user.user_id))
            return UserProfile(user, res[0], res[1] )

async def main():

    p = ProfileService()
    USER_ID = 1
    start = time.perf_counter()
    try:
        friends = await p.get_profile(USER_ID)
        print(f"elapsed time: {time.perf_counter() - start}")
        print(friends)
    except TimeoutError as E:
        print("Request timed out!")
    except Exception as e:
        print(f"Unknown exception: {e}")


    

if __name__ == "__main__":
    asyncio.run(main())
