from faker import Faker
from threaddit import app, db
from threaddit.users.models import User
from threaddit.subthreads.models import Subthread
from threaddit.posts.models import Posts
from threaddit.comments.models import Comments
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
    "Technology Updates": {
        "posts": [
            {"title": "Is 5G really as revolutionary as we’re told?", "comments": [
                "I think 5G will change mobile internet, but it’s overhyped right now.",
                "5G is great for streaming and gaming, but I think it needs more infrastructure.",
                "I’m excited to see how 5G affects smart cities and IoT devices.",
                "I don’t think 5G will be a game-changer until it’s more widely available.",
                "5G is definitely going to make a huge difference in tech in the next few years."
            ]},
            {"title": "What’s the future of Artificial Intelligence in 10 years?", "comments": [
                "AI will definitely automate a lot of jobs, but new jobs will also emerge.",
                "In 10 years, I think AI will be more integrated into daily life and more ethical.",
                "AI will have a massive impact on healthcare, but privacy concerns will also rise.",
                "AI in education could transform the way we learn and teach.",
                "I’m excited about AI in creative fields like music and art, it’s going to be revolutionary."
            ]},
            {"title": "How long until self-driving cars become mainstream?", "comments": [
                "Self-driving cars are close, but I think regulatory hurdles are still an issue.",
                "I believe autonomous vehicles will become mainstream in the next 10 years.",
                "With more testing, self-driving cars could reduce accidents caused by human error.",
                "The technology is improving, but I’m not sure if it’s safe enough yet.",
                "I think self-driving cars will be a common sight in major cities within 5 years."
            ]}
        ]
    },
    "Food & Drink": {
        "posts": [
            {"title": "What’s your favorite comfort food?", "comments": [
                "Mac and cheese is my ultimate comfort food.",
                "Pizza is always my go-to when I'm feeling down.",
                "Ramen has a special place in my heart, especially on cold days.",
                "Nothing beats a warm bowl of soup during winter.",
                "Lasagna is always a family favorite, it’s hearty and satisfying."
            ]},
            {"title": "How do you feel about vegan food?", "comments": [
                "I’ve tried a few vegan dishes and really liked them.",
                "Vegan food can be hit or miss, but I’ve found some great recipes.",
                "I think vegan food is delicious, it’s all about the spices and flavors.",
                "I’m not vegan, but I enjoy plant-based meals from time to time.",
                "Some vegan recipes are fantastic, especially when they mimic meat dishes."
            ]},
            {"title": "What’s your go-to coffee order?", "comments": [
                "I always go for a caramel macchiato, it’s my favorite.",
                "I’m a black coffee person, simple and strong.",
                "I love a good cold brew with almond milk, so refreshing!",
                "Espresso is my drink of choice for a quick energy boost.",
                "I’m a huge fan of flat whites, they have the perfect balance."
            ]}
        ]
    },
    "Books & Literature": {
        "posts": [
            {"title": "What’s the best book you’ve read this year?", "comments": [
                "'The Midnight Library' was incredible, such a unique perspective on life.",
                "'Atomic Habits' changed my perspective on forming good habits.",
                "'Man’s Search for Meaning' by Viktor Frankl is life-changing.",
                "I loved 'Educated' by Tara Westover, it was inspiring and emotional.",
                "'Dare to Lead' by Brené Brown is an empowering read."
            ]},
            {"title": "Who’s your favorite classic author?", "comments": [
                "I love Charles Dickens, his characters are so rich and relatable.",
                "Jane Austen is my favorite, I enjoy her sharp wit and social commentary.",
                "Shakespeare is the ultimate, his plays are timeless.",
                "Mark Twain’s humor and insight into human nature is unmatched.",
                "Hemingway’s style is so unique, and his stories are unforgettable."
            ]},
            {"title": "What genre do you enjoy the most?", "comments": [
                "I’m into fantasy, it’s an escape from reality for me.",
                "I enjoy non-fiction, especially history and self-improvement.",
                "Thrillers keep me hooked, I love books that make me think.",
                "Science fiction is my go-to, I love exploring new worlds and ideas.",
                "Historical fiction is fascinating, especially books set in World War II."
            ]}
        ]
    }
}

# Function to generate 20 users with actual names
def generate_users():
    users = []
    for i in range(1, 21):  # Generate 20 users
        name = fake.name()
        email = fake.email()
        password_hash = generate_password_hash("password")  # Hash the password securely
        user = User(username=name.split()[0], email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        users.append(user)
    return users

# Function to seed the database with the threads, posts, comments, and users
def seed():
    with app.app_context():
        # Create 20 users
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
