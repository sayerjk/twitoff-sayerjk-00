from os import getenv
from .models import DB, Tweet, User
import tweepy
import spacy

# Get API keys
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Authenticate with twitter
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)

# Open a connection to the API
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    try:
        # GET user data from Twitter
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if user is in database
        # if User in DB, do nothing
        # if User not in DB, insert into DB
        db_user = (
            User.query.get(twitter_user.id) or 
            User(id=twitter_user.id, username=username)
        )

        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200, 
            exclude_replies=True, 
            include_rts=False, 
            tweet_mode='extended',
            since_id=db_user.newest_tweet_id)

        # assign newest_tweet_id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add the individual tweets to the DB
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id, 
                text=tweet.full_text[:300],
                user_id=db_user.id,
                vect=tweet_vector)
            
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    # Final step: Save (commit) changes
    except Exception as error:
        print(f'Error when processing {username}: {error}')
        raise error
        
    else: 
        DB.session.commit()

nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
