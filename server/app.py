#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles]), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views in the session if not already set
    session['page_views'] = session.get('page_views', 0)

    # Increment the page_views count
    session['page_views'] += 1

    # Check if the user has exceeded the maximum number of allowed page views
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Return the article data if within the allowed page views limit
    article = Article.query.get_or_404(id)
    return jsonify(article.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555)
