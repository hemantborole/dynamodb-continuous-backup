* pip install --upgrade boto3 awscli hjson shortuuid
* Use updated source code from https://github.com/hemantborole/dynamodb-continuous-backup.git
* Create Roles
    * CloudWatchEventsRole - CloudWatch Events from CloudWatchEventsInvocationAccess - events.amazonaws.com
        file cloudwatchevents_role.json
    * firehose_delivery_role - IAM Role that Kinesis Firehose will use to write to S3 - firehose.amazonaws.com
        Create a S3 bucket for incremental backups.
        edit file firehose_trust.json for s3 bucket and account number.
    * LambdaExecRole - IAM Role that AWS Lambda uses to write to Kinesis Firehose - lambda.amazonaws.com
        use file lambdaexecrole.json
* Edit the src/config.hjson
* Execute build.sh to create the lambda functions.
  ```
  cd src
  ./build.sh config.hjson
  This creates ../dist/dynamodb_continuous_backup-1.1.zip
  ```
* Execute deploy.py
  ```
  cd src
  ./deploy.py --config-file config.hjson
  ```
* Edit provisioning_whitelist.hjson to add list of existing tables
  ```
  cd src
  python setup_existing_tables.py --region us-west-2 --profile dungeon --table-list provisioning_whitelist.hjson
  ```
