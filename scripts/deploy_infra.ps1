aws cloudformation deploy --template-file .\TgtgPoller_stack.json --stack-name TgTgPoller --capabilities CAPABILITY_NAMED_IAM --profile Personal

Write-Output "Infrastructure deployed successfully"
