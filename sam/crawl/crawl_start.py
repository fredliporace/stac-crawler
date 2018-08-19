"""crawl_start"""

import os
import boto3

SQS_CLIENT = boto3.client('sqs')

def start_crawl(root_catalog_url, to_be_visited_queue):
    """
    Inserts the first catalog in to-be-visited Queue
    """
    SQS_CLIENT.send_message(QueueUrl=to_be_visited_queue,
                            MessageBody=root_catalog_url)
    print('Inserting root catalog', root_catalog_url)

def handler(event, context):
    """Lambda entry point
    Event keys:
      root_catalog: crawl starts from this URL, children catalogs only
    Environment vars:
      CATALOG_CRAWL_QUEUE: SQS used to store nodes to be visited
    """

    return start_crawl(root_catalog_url=event['root_catalog'],
                       to_be_visited_queue=os.environ['CATALOG_CRAWL_QUEUE'])
