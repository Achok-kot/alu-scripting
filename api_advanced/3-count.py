#!/usr/bin/python3
"""Module to recursively query Reddit API and count keywords"""
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """Recursively counts keywords in hot article titles"""
    if word_count is None:
        word_count = {}
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "python:subreddit.count:v1.0"}
    params = {"after": after, "limit": 100} if after else {"limit": 100}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])
    after = data.get("after")

    for post in posts:
        title = post.get("data", {}).get("title", "").lower().split()
        for word in title:
            if word in word_count:
                word_count[word] += 1

    if after:
        return count_words(subreddit, word_list, after, word_count)

    sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        if count > 0:
            print(f"{word}: {count}")
