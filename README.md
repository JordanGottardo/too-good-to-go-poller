# too-good-to-go-poller

# Create venv

`python -m venv venv`
`pip install -r requirements.txt`

# Run app locally

`uvicorn main:app --reload`

## Via docker-coompose

`docker-compose up lambda-fastapi-dev`

# Deploy infrastructure

-   Deploy prereq (ECR):
    `aws cloudformation deploy --template-file .\TgtgPoller_ecr_stack.json --stack-name TgTgPollerPrereq --capabilities CAPABILITY_NAMED_IAM --profile Personal`

-   Deploy rest of infra (NoSQL Workbench used to model DynamoDB tables)
    `aws cloudformation deploy --template-file .\TgtgPoller_stack.json --stack-name TgTgPoller --capabilities CAPABILITY_NAMED_IAM --profile Personal`

# Guide to deploy FastApi as Docker image to Lambda

https://rafrasenberg.com/posts/deploying-fastapi-on-aws-as-a-lambda-container-image/
