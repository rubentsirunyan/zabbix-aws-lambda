# zabbix-aws-lambda
AWS Lambda function to manage AWS EC2 instances as Zabbix hosts.

# Install the dependencies

Install `zabbix-api` as a dependency as described [here](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html).

# Set up the environment

Set the environment variables in AWS Console as described [here](https://docs.aws.amazon.com/lambda/latest/dg/env_variables.html).

```bash
ZBX_SERVER_URL="<Zabbix server URL>"
ZBX_LOGIN_USER="<Zabbix server login user>"
ZBX_LOGIN_PASSWORD="<Zabbix server login password>"
ZBX_VALIDATE_CERTS="<Validate Zabbix server SSL certificates>"
```
