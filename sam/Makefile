# The following parameters must be defined for yours
# installation. They may be set in a
# local deploy_parameters.make file
DEPLOY_BUCKET = YOUR_DEPLOY_BUCKET_NAME
STAC_ITEM_TOPIC = ARN_OF_SNS_TOPIC_THAT_RECEIVES_CRAWLED_STAC_ITEMS

-include deploy_parameters.make

# Primary
APP = stac-crawler
STACK_NAME = stac-crawler

# Derived
SAM_TEMPLATE = $(APP)-template.yaml
SAM_PACKAGED = $(APP)-packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://$(SAM_TEMPLATE)

package:
	aws cloudformation package --template-file $(SAM_TEMPLATE) --s3-bucket $(DEPLOY_BUCKET) --output-template $(SAM_PACKAGED) 

deploy: validate package
	aws cloudformation deploy --template-file $(SAM_PACKAGED) --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM --parameter-overrides StacItemTopic=$(STAC_ITEM_TOPIC)
