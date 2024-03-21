# pylint: disable=no-value-for-parameter
"""
Client of the Wagon OpenGraph API
"""

import requests

def fetch_metadata(url):
    """
    Return a dictionary of OpenGraph metadata found in HTML of given url
    """
    baseurl = "https://opengraph.lewagon.com/?url="
    response = requests.get(baseurl+url)
    if response.status_code != 200:
        return {}

    return response.json()["data"]
