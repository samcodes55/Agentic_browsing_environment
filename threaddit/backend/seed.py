

# from threaddit import app, db
# from threaddit.users.models import User
# from threaddit.subthreads.models import Subthread
# from threaddit.posts.models import Posts
# from threaddit.comments.models import Comments
# from random import choice
# from werkzeug.security import generate_password_hash  # To hash passwords securely
# from datetime import datetime

# # Normal, relevant content for posts and comments based on the subthread
# THREAD_NAMES = {
#     "Health & Fitness": {
#         "posts": [
#             {"title": "What’s your favorite home workout?", "comments": [
#                 "I love doing bodyweight exercises like push-ups and squats.",
#                 "Yoga is great for flexibility and relaxation, it’s my favorite.",
#                 "I prefer weight training for building strength at home.",
#                 "HIIT workouts have really helped me improve my stamina.",
#                 "I do a lot of calisthenics, I find it both challenging and rewarding.",
#                 "Pilates has been great for strengthening my core.",
#                 "Running is great for overall fitness and mental clarity."
#             ]},
#             {"title": "How often do you change your workout routine?", "comments": [
#                 "I switch up my routine every 6-8 weeks to avoid plateaus.",
#                 "I like to change things every month, keeps me motivated.",
#                 "I rarely change it, I focus on consistent progress with my current plan.",
#                 "Every 3-4 months, I make slight adjustments to my routine.",
#                 "I love experimenting with different workout styles, like strength, HIIT, and yoga.",
#                 "I prefer sticking with a routine for 6 months and then reassessing."
#             ]},
#             {"title": "How do you track your fitness progress?", "comments": [
#                 "I use a fitness app to log my workouts and track calories.",
#                 "I take progress pictures and track my strength gains.",
#                 "I keep a fitness journal to log my progress weekly.",
#                 "I track my weight and take measurements every month to check progress.",
#                 "I use my smartwatch to monitor heart rate and steps.",
#                 "I track personal bests for lifts and running times to gauge improvements."
#             ]}
#         ]
#     },
#     "Tech Gadgets": {
#         "posts": [
#             {"title": "What’s the most useful gadget you own?", "comments": [
#                 "My smartwatch helps me stay on top of notifications and health.",
#                 "A noise-cancelling headphone is a must-have for me during travel.",
#                 "I love my smart speaker, it controls everything in my house.",
#                 "My fitness tracker has been invaluable in monitoring my daily activity.",
#                 "The wireless earbuds are so convenient for music on the go.",
#                 "A portable power bank is something I always have with me."
#             ]},
#             {"title": "How do you feel about foldable phones?", "comments": [
#                 "Foldable phones are innovative, but I’m waiting for them to be more durable.",
#                 "I think they’re cool, but not practical enough for daily use yet.",
#                 "I’m not sold on foldable phones, they seem gimmicky to me.",
#                 "I’m intrigued, but I think the price point is still too high.",
#                 "It’s interesting to see the evolution of phone designs, but I’ll stick to a regular one for now.",
#                 "I believe foldable phones have a bright future, but the technology needs refinement."
#             ]},
#             {"title": "What tech product are you most excited about?", "comments": [
#                 "I’m looking forward to the next-gen VR headsets, they’re getting better every year.",
#                 "I'm excited about advancements in AR glasses, could change the way we interact with the world.",
#                 "The new AI chips are really exciting, they will take machine learning to the next level.",
#                 "I can’t wait to see the next update in wearable technology, especially in health tracking.",
#                 "The future of 5G technology is very exciting, especially with IoT devices."
#             ]}
#         ]
#     },
#     "Food & Cooking": {
#         "posts": [
#             {"title": "What’s your go-to comfort food?", "comments": [
#                 "I love mac and cheese, it’s the ultimate comfort food.",
#                 "Pizza is always my go-to when I need something comforting.",
#                 "I go for a big bowl of ramen, it’s always comforting after a tough day.",
#                 "Nothing beats a warm bowl of soup during winter.",
#                 "Lasagna is always a family favorite, it’s hearty and satisfying.",
#                 "I love a good homemade chicken pot pie, so nostalgic."
#             ]},
#             {"title": "What’s the best dish to cook for beginners?", "comments": [
#                 "Scrambled eggs are easy to make and a good starting point.",
#                 "Pasta with marinara sauce is simple and delicious for beginners.",
#                 "Stir-fried veggies with rice is quick, healthy, and easy to make.",
#                 "Baked chicken with vegetables is foolproof for beginners.",
#                 "Tacos are great, and you can get creative with the fillings.",
#                 "I think fried rice is a perfect beginner’s dish, it’s easy and quick."
#             ]},
#             {"title": "How do you prepare a healthy breakfast?", "comments": [
#                 "I like to have oatmeal with fruits and a protein shake.",
#                 "Smoothies with greens and protein powder are my go-to.",
#                 "I prepare avocado toast with eggs for a filling and healthy breakfast.",
#                 "Greek yogurt with honey, chia seeds, and granola is my usual choice.",
#                 "I make overnight oats the night before, it’s ready in the morning and super nutritious.",
#                 "I go for scrambled eggs with spinach and whole wheat toast."
#             ]}
#         ]
#     },
#     "Books & Literature": {
#         "posts": [
#             {"title": "What’s the most inspiring book you’ve read?", "comments": [
#                 "'The Power of Now' really helped me become more mindful and present.",
#                 "'Atomic Habits' changed my perspective on forming good habits.",
#                 "'Man’s Search for Meaning' by Viktor Frankl is life-changing.",
#                 "I found 'Dare to Lead' by Brené Brown incredibly inspiring.",
#                 "Reading 'The Alchemist' gave me a fresh perspective on pursuing my dreams.",
#                 "'Educated' by Tara Westover was both heartbreaking and inspiring."
#             ]},
#             {"title": "Who’s your favorite classic author?", "comments": [
#                 "I love Charles Dickens, his characters are so rich and relatable.",
#                 "Jane Austen is my favorite, I enjoy her sharp wit and social commentary.",
#                 "Shakespeare is the ultimate, his plays are timeless.",
#                 "I have a soft spot for Mark Twain, his works are full of humor and wisdom.",
#                 "Hemingway’s style is so unique, and his stories are unforgettable."
#             ]},
#             {"title": "What genre do you enjoy the most?", "comments": [
#                 "I’m into fantasy, it’s an escape from reality for me.",
#                 "I enjoy non-fiction, especially history and self-improvement.",
#                 "Thrillers keep me hooked, I love books that make me think.",
#                 "Science fiction is my go-to, I love exploring new worlds and ideas.",
#                 "Historical fiction is fascinating, especially when it’s based on real events."
#             ]}
#         ]
#     }
#     # You can continue adding more threads and posts for other topics
# }



# def seed():
#     with app.app_context():
#         # --- Create multiple users ---
#         users = []
#         for i in range(1, 6):  # Create 5 users
#             user = User.query.filter_by(id=i).first()
#             if not user:
#                 print(f"[NEW] Creating user{i}")
#                 # Password is hashed before being stored
#                 password_hash = generate_password_hash("password")
#                 user = User(
#                     username=f"user{i}", 
#                     email=f"user{i}@example.com", 
#                     password_hash=password_hash,  # Store hashed password
#                     avatar="https://www.example.com/avatar.png",  # Dummy avatar
#                     bio="Just another user."  # Dummy bio
#                 )
#                 db.session.add(user)
#                 db.session.commit()
#             users.append(user)

#         # --- Create threads and posts ---
#         for thread_name, thread_data in THREAD_NAMES.items():
#             # Add 't/' prefix to the subthread name
#             formatted_thread_name = f"t/{thread_name}"

#             # Create a subthread (category)
#             subthread = Subthread.query.filter_by(name=formatted_thread_name).first()

#             if subthread:
#                 print(f"[EXISTS] Subthread: {formatted_thread_name} (ID {subthread.id})")
#             else:
#                 print(f"[NEW] Creating subthread: {formatted_thread_name}")
#                 subthread = Subthread(
#                     name=formatted_thread_name,
#                     logo="https://i.ibb.co/3WddYZZ/hacker.png",  # Random image URL (can change)
#                     created_by=choice(users).id  # Random user as creator
#                 )
#                 db.session.add(subthread)
#                 db.session.commit()

#             # Create posts under the subthread
#             for post_data in thread_data["posts"]:
#                 post_title = post_data["title"]
#                 post_comments = post_data["comments"]

#                 # Check if post already exists to avoid duplicates
#                 existing_post = Posts.query.filter_by(
#                     subthread_id=subthread.id,
#                     title=post_title
#                 ).first()

#                 if existing_post:
#                     print(f"    [EXISTS] Post already in subthread: {post_title}")
#                     continue

#                 print(f"    [NEW] Creating post: {post_title} in subthread: {formatted_thread_name}")
#                 post_content = choice(post_comments)  # Use one of the relevant comments as post content
#                 post = Posts(
#                     user_id=choice(users).id,  # Random user posts
#                     subthread_id=subthread.id,
#                     title=post_title,
#                     content=post_content
#                 )
#                 db.session.add(post)
#                 db.session.commit()  # Commit to the database after each post

#                 # --- Add Comments to Posts ---
#                 for comment_content in post_comments:  # Use all comments for this post
#                     print(f"        Adding comment to post: {post.title}")
#                     comment = Comments(
#                         post_id=post.id,
#                         user_id=choice(users).id,  # Random user commenting
#                         content=comment_content
#                     )
#                     db.session.add(comment)

#                 db.session.commit()  # Commit all comments after adding them to the post

#         print("\nDONE SEEDING\n")


# if __name__ == "__main__":
#     seed()
from faker import Faker
from threaddit import app, db
from threaddit.users.models import User
from threaddit.subthreads.models import Subthread
from threaddit.posts.models import Posts
from threaddit.comments.models import Comments  # Correct import for the class
from werkzeug.security import generate_password_hash  # To hash passwords securely
from random import choice, randint

# Initialize Faker to generate fake user data
fake = Faker()

# List of new thread names
THREAD_NAMES = {
    "Sports Discussions": {
        "posts": [
            {"title": "Who is going to win the next football World Cup?", "comments": [
                "I think Brazil will take it this time.", 
                "I’m rooting for Argentina, they have a great team.",
                "The next World Cup will be interesting, especially with the new teams qualifying.",
                "I can see France winning again, they have a solid squad.",
                "Germany always comes up with surprises in big tournaments."
            ]},
            {"title": "What are your thoughts on the new NBA season?", "comments": [
                "I’m excited to see the Lakers perform this season!",
                "The Bucks have a chance to win again, Giannis is unstoppable.",
                "I’m hoping for an underdog team to break through this season.",
                "I believe the Nets have a strong chance this year.",
                "The NBA has really leveled up in terms of talent this season."
            ]},
            {"title": "Which esports game is the most popular right now?", "comments": [
                "League of Legends is still the king of esports.",
                "Valorant is making waves, especially in competitive esports.",
                "Dota 2’s international tournaments are unmatched in prize pools.",
                "Counter-Strike: Global Offensive is still one of the biggest.",
                "PUBG Mobile has really taken off in recent years."
            ]}
        ]
    },
    # Add other thread data here (Technology Updates, Food & Drink, etc.)
}

# Function to generate unique users (ensuring no duplicate usernames)
def generate_users():
    users = []
    for i in range(1, 21):  # Generate 20 users
        name = fake.name()
        email = fake.email()
        username = name.split()[0]  # Using the first name as the username
        
        # Ensure username is unique
        while User.query.filter_by(username=username).first():
            username = f"{username}{randint(1, 999)}"  # Append a random number if username exists

        password_hash = generate_password_hash("password")  # Hash the password securely
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        users.append(user)
    return users

# Function to seed the database with the threads, posts, comments, and users
def seed():
    with app.app_context():
        # Create 20 unique users
        users = generate_users()

        # Create 10 threads and add posts and comments
        for thread_name, thread_data in THREAD_NAMES.items():
            formatted_thread_name = f"t/{thread_name}"

            # Check if the thread exists
            subthread = Subthread.query.filter_by(name=formatted_thread_name).first()

            if not subthread:
                subthread = Subthread(name=formatted_thread_name, created_by=choice(users).id)
                db.session.add(subthread)
                db.session.commit()

            # Create posts for each thread
            for post_data in thread_data["posts"]:
                post_title = post_data["title"]
                post_comments = post_data["comments"]

                # Check if the post exists
                existing_post = Posts.query.filter_by(subthread_id=subthread.id, title=post_title).first()

                if not existing_post:
                    post_content = choice(post_comments)  # Randomly select one comment as the post content
                    post = Posts(user_id=choice(users).id, subthread_id=subthread.id, title=post_title, content=post_content)
                    db.session.add(post)
                    db.session.commit()

                    # Add comments to the post
                    for _ in range(randint(3, 10)):  # Each post gets between 3 to 10 comments
                        comment_content = choice(post_comments)
                        comment = Comments(post_id=post.id, user_id=choice(users).id, content=comment_content)
                        db.session.add(comment)

                    db.session.commit()

        print("\nDONE SEEDING\n")

# Run the seeding function
if __name__ == "__main__":
    seed()
