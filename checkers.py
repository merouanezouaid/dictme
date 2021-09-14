import os
import requests
import urllib.parse
import json

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def errorCheck(word):
    """handle errors"""
    # Contact API

    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word + "/"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        r = response.json()
        return {
            "phonetic" : r[0]["phonetic"],
            "origin" : r[0]["origin"],
            "definition" : r[0]["meanings"][0]["definitions"][0]["definition"],
            "audio" : r[0]["phonetics"][0]["audio"]
        }
    except (KeyError, TypeError, ValueError):
        return None