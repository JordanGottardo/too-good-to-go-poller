aws cloudformation deploy --template-file .\TgtgPoller_ecr_stack.json --stack-name TgTgPollerPrereq --capabilities CAPABILITY_NAMED_IAM  --profile Personal

Write-Output "ECR repository created successfully, ensure the right ECR URI is set in TgtgPoller_stack.json"