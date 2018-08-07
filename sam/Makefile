# Required env vars
# DEPLOY_BUCKET

# Primary
APP = stac-crawler
STACK_NAME = stac-crawler

# Derived
SAM_TEMPLATE = $(APP)-template.yaml
SAM_PACKAGED = $(APP)-packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://$(SAM_TEMPLATE)

package:
	aws cloudformation package --template-file $(SAM_TEMPLATE) --s3-bucket ${DEPLOY_BUCKET} --output-template $(SAM_PACKAGED) 

deploy: validate package
	aws cloudformation deploy --template-file $(SAM_PACKAGED) --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM
