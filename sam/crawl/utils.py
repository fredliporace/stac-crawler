"""utililities for stac crawling"""

import json
from urllib.request import urlopen

def url_to_json(url: str):
    """
    Download and return the JSON object referenced by url

    :param url: URL to be downloaded
    """

    with urlopen(url) as furl:
        content = furl.read()
    return json.loads(content)

def get_links(catalog: json, url: str):
    """
    Return a list of children catalogs and items for a given STAC catalog
    represented as a JSON object.

    :param catalog: STAC catalog as a JSON object
    :param url: originating URL of the item, used to build the complete
                URL for children

    Return: children and items list
    """
    children = list()
    items = list()
    part = url.rpartition('/')
    base_url = part[0] + part[1]
    for link in catalog['links']:
        if link['rel'] == 'child':
            children.append(base_url + link['href'])
        if link['rel'] == 'item':
            items.append(base_url + link['href'])
    return children, items
