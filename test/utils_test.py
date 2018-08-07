"""utils_test"""

import json
import unittest

from sam.crawl.utils import url_to_json, get_children_links

def file_as_json(filename):
    """
    Return local file as JSON object
    """
    with open(filename, 'r') as fptr:
        content = fptr.read()
    return json.loads(content)

class UtilsTest(unittest.TestCase):
    """UtilsTest"""

    def test_url_to_json(self):
        """test_url_to_json"""

        jobject = url_to_json('https://s3.amazonaws.com/cbers-stac/CBERS4/catalog.json')
        self.assertEqual(jobject['name'], 'CBERS4')

    def test_get_children_links(self):
        """test_get_children_links"""

        clinks = get_children_links(file_as_json('test/CBERS4_root.json'),
                                    'https://s3.amazonaws.com/cbers-stac/CBERS4/catalog.json')
        self.assertEqual(len(clinks), 2)
        self.assertTrue('https://s3.amazonaws.com/cbers-stac/CBERS4/MUX/catalog.json' in clinks)
        self.assertTrue('https://s3.amazonaws.com/cbers-stac/CBERS4/AWFI/catalog.json' in clinks)
        self.assertFalse('https://s3.amazonaws.com/cbers-stac/CBERS4/PAN/catalog.json' in clinks)

if __name__ == '__main__':
    unittest.main()
