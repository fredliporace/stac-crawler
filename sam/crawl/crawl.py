"""crawl"""

import os
import json
import boto3

from utils import url_to_json, get_links

SQS_CLIENT = boto3.client('sqs')

SNS_CLIENT = boto3.client('sns')

def crawl(records, to_be_visited_queue, item_topic_arn, max_children=999):
    """
    Consume catalog from queue and insert children for
    future visit

    Input:
      records(list): catalogs to be visited
      to_be_visiited_queue(string): SQS to insert children
      item_sns_arn: ARN of SNS topic that receives the STAC items
      max_children(int): maximum number of children to be visited
    """

    for record in records:
        catalog = url_to_json(record['body'])
        clinks, items = get_links(catalog, record['body'])
        # Children catalogs are placed into the queue to be visited
        for index, clink in enumerate(clinks):
            if index == max_children:
                break
            SQS_CLIENT.send_message(QueueUrl=to_be_visited_queue,
                                    MessageBody=clink)
            print('Catalog inserted: ', clink)
        # Items are sent to SNS topic
        for item in items:
            json_item = url_to_json(item)
            SNS_CLIENT.publish(TargetArn=item_topic_arn,
                               Message=json.dumps(json_item))

def handler(event, context):
    """Lambda entry point
    Event keys:
      Records: catalog links to be visited
    Environment vars:
      CATALOG_CRAWL_QUEUE: SQS used to store nodes to be visited
    """

    return crawl(event['Records'],
                 to_be_visited_queue=os.environ['CATALOG_CRAWL_QUEUE'],
                 item_topic_arn=os.environ['STAC_ITEM_TOPIC'],
                 max_children=int(os.environ['MAX_CHILDREN']))
