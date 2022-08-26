# too-good-to-go-poller

# Create venv
```python -m venv venv```
```pip install -r requirements.txt```

# Run app locally
```uvicorn main:app --reload```

# Deploy infrastructure
NoSQL Workbench used to model DynamoDB tables

```aws cloudformation deploy --template-file .\TgtgPoller_stack.json --stack-name TgTgPoller  --capabilities CAPABILITY_NAMED_IAM --profile Personal```

Prereq (ECR):
```aws cloudformation deploy --template-file .\TgtgPoller_ecr_stack.json --stack-name TgTgPollerPrereq --capabilities CAPABILITY_NAMED_IAM  --profile Personal```