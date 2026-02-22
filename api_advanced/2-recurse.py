#!/usr/bin/python3
"""Module to recursively query Reddit API for all hot articles"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Recursively returns a list of titles of all hot articles"""
    if hot_list is None:
        hot_list = []
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "python:subreddit.recurse:v1.0"}
    params = {"after": after, "limit": 100} if after else {"limit": 100}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code == 200:
        data = response.json().get("data", {})
        posts = data.get("children", [])
        after = data.get("after")
        hot_list.extend([post.get("data", {}).get("title") for post in posts])
        if after:
            return recurse(subreddit, hot_list, after)
        return hot_list
    return None
