"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime
import json

from app.utils.redis import REDIS_CLIENT


@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def _json_to_article(json: dict) -> Article:

    author=json.get("author", "Unknown")
    title=json.get("title")
    body=json.get("text")
    publish_date=datetime.fromisoformat(json.get("published"))
    image_url=json.get("main_image")
    url=json.get("url")

    return Article(author, title, body, publish_date, image_url, url)


def get_all_news() -> list[Article]:
    """Get all news articles from the datastore."""
    # 1. Use Redis client to fetch all articles
    # 2. Format the data into articles
    # 3. Return a list of the articles formatted 

    # Get all articles from Redis ("all_articles" put in redis stream in __init__.py)
    all_articles = REDIS_CLIENT.get_entry("all_articles")
    
    # Put all articles into a list of articles
    articles = []
    for article in all_articles:
        articles.append(_json_to_article(article))

    # Return list of articles
    return articles


def get_featured_news() -> list[Article] | None:
    """Get the featured news article from the datastore."""
    # 1. Get all the articles
    # 2. Return as a list of articles sorted by most recent date
    # "Featured" just means most recent

    # Get all articles
    all_articles = get_all_news()

    # Sort articles by most recent date
    # Return the most recent article or None if no articles exist
    return sorted(all_articles, 
                  key=lambda article: article.publish_date, 
                  reverse=True) if all_articles else None
