"""utils_test"""

import json
import unittest

from sam.crawl.utils import url_to_json, get_links

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

    def test_get_links(self):
        """test_get_links"""

        clinks, items = get_links(file_as_json('test/CBERS4_root.json'),
                                  'https://s3.amazonaws.com/cbers-stac/CBERS4/catalog.json')
        self.assertEqual(len(clinks), 2)
        self.assertEqual(len(items), 0)
        self.assertTrue('https://s3.amazonaws.com/cbers-stac/CBERS4/MUX/catalog.json' in clinks)
        self.assertTrue('https://s3.amazonaws.com/cbers-stac/CBERS4/AWFI/catalog.json' in clinks)
        self.assertFalse('https://s3.amazonaws.com/cbers-stac/CBERS4/PAN/catalog.json' in clinks)

        clinks, items = get_links(file_as_json('test/catalog-with-item.json'),
                                  'https://s3.amazonaws.com/cbers-stac/CBERS4/AWFI/062/093/'
                                  'catalog.json')
        self.assertEqual(len(clinks), 0)
        self.assertEqual(len(items), 1)
        self.assertTrue('https://s3.amazonaws.com/cbers-stac/CBERS4/AWFI/062/093/'
                        'CBERS_4_AWFI_20180411_062_093_L2.json' in items)

if __name__ == '__main__':
    unittest.main()
