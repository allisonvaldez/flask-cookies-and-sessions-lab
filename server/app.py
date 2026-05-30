#!/usr/bin/env python3

# Import necessary components to run app
from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User, ArticleSchema, UserSchema

# Create Flask, initilize configuration, create db
app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Connects Flask-Migrate to Flask app and SQLAlchemy db for allowing database migration commands
migrate = Migrate(app, db)
db.init_app(app)

# Create route to clear session
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Create route for articles
@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

# Create route for a single article based on id
@app.route('/articles/<int:id>')
def show_article(id):
    # Control logic and error handling
    if "page_views" not in session:
        session["page_views"] = 0

    # Increment page view every time route is hit
    session["page_views"] += 1

    # Paywall logic of 3 articles viewed
    if session["page_views"] > 3:
        return make_response(
            jsonify({'message': 'Maximum pageview limit reached'}), 401
        )
    
    # Otherwise look up the article in the db by id
    article = Article.query.filter(Article.id == id).first()

    # Serialize article object into jsonified dictionary
    article_data = ArticleSchema().dump(article)

    # Send serialized article as a response back
    return make_response(article_data, 200)


if __name__ == '__main__':
    app.run(port=5555)
