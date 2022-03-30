from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):


    # Query for the two users from the DB
    user0= User.query.filter(User.username== user0_username).one()
    user1= User.query.filter(User.username== user1_username).one()

    # Access vectorizations
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine vectorization into our X-matrx (training set)
    X = np.vstack([user0_vects, user1_vects])

    # Generate 0s and 1s to serve as y-vector (test set)
    y = np.concatenate([
        np.zeros(len(user0.tweets)), 
        np.ones(len(user1.tweets))])

    # TRAIN MODEL: Logistic Regression
    log_reg = LogisticRegression()
    log_reg.fit(X, y)

    # get WORD EMBEDDING (vectorization) for hypo tweet
    hypo_tweet_vect = np.array([vectorize_tweet(hypo_tweet_text)])

    prediction = log_reg.predict(hypo_tweet_vect)

    return prediction[0]
