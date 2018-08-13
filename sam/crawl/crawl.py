"""crawl"""

import os
import boto3

from utils import url_to_json, get_children_links

SQS_CLIENT = boto3.client('sqs')

def crawl(records, to_be_visited_queue, max_children=999):
    """
    Consume catalog from queue and insert children for
    future visit

    Input:
      records(list): catalogs to be visited
      to_be_visiited_queue(string): SQS to insert children
      max_children(int): maximum number of children to be visited
    """

    for record in records:
        catalog = url_to_json(record['body'])
        clinks = get_children_links(catalog, record['body'])
        for index, clink in enumerate(clinks):
            if index == max_children:
                break
            SQS_CLIENT.send_message(QueueUrl=to_be_visited_queue,
                                    MessageBody=clink)
            print('Catalog inserted: ', clink)

def handler(event, context):
    """Lambda entry point
    Event keys:
      Records: catalog links to be visited
    Environment vars:
      CATALOG_CRAWL_QUEUE: SQS used to store nodes to be visited
    """

    return crawl(event['Records'],
                 to_be_visited_queue=os.environ['CATALOG_CRAWL_QUEUE'],
                 max_children=int(os.environ['MAX_CHILDREN']))
