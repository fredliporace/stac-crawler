"""utililities for stac crawling"""

import json
from urllib.request import urlopen

def url_to_json(url):
    """
    Download and return the JSON object referenced by url
    """

    with urlopen(url) as furl:
        content = furl.read()
    return json.loads(content)

def get_children_links(stac_item, url):
    """
    Return a list of children items for a given STAC item
    represented as a JSON object.
    Input:
      stac_item: STAC item as a JSON object
      url: originating URL of the item, used to build the complete
           URL for children
    """
    children = list()
    part = url.rpartition('/')
    base_url = part[0] + part[1]
    for link in stac_item['links']:
        if link['rel'] == 'child':
            children.append(base_url + link['href'])
    return children
