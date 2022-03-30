from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user, vectorize_tweet

def create_app():

    app = Flask(__name__)

    # Tell our app where to find our database
    # "registering" our database with app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

#  ===================================================================

    @app.route("/")
    def home():

        users = User.query.all()

        print(users, flush=True)

        return render_template('base.html', title="home", users=users)

    @app.route("/another")
    def another():
        return render_template('base.html', title='another')

#  ===================================================================

    @app.route('/reset')
    def reset():

        # drop DB tables
        DB.drop_all()
        # creates tables according to classes in models.py
        DB.create_all()

        tweet1_vector = vectorize_tweet('Wow...')
        tweet2_vector = vectorize_tweet('Woah...')

        sayer = User(id=1, username='sayer')
        neo = User(id=2, username='neo')

        tweet1 = Tweet(id=1, text='Wow...', user=sayer, vect=tweet1_vector)        
        tweet2 = Tweet(
            id=2, text='Woah...',
            user=neo, vect=tweet2_vector)

        DB.session.add(sayer)
        DB.session.add(neo)
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.commit()

        return render_template('base.html', title='Reset DB')

#  ===================================================================

    @app.route('/populate')
    def populate():

        add_or_update_user('nasa')
        add_or_update_user('joerogan')
        add_or_update_user('MobyQuotes') 

        DB.session.commit()

        return render_template('base.html', title='Populate')

#  ===================================================================

    @app.route('/update')
    def update():
        usernames = [user.username for user in User.query.all()]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='Update')

    return app
    