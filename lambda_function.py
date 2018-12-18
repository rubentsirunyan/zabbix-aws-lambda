from __future__ import print_function

import os
from zabbix_api import ZabbixAPI
import boto3


print('Loading function')

zbx_server_url = os.environ.get('ZBX_SERVER_URL')
zbx_login_user = os.environ.get('ZBX_LOGIN_USER')
zbx_login_password = os.environ.get('ZBX_LOGIN_PASSWORD')
zbx_validate_certs = os.environ.get('ZBX_VALIDATE_CERTS', 'false').lower() in ['true', 'yes', '1']

zapi = ZabbixAPI(zbx_server_url, timeout=10, validate_certs=zbx_validate_certs)
zapi.login(zbx_login_user, zbx_login_password)


def aws_get_instance_info(_id, _region):
    client = boto3.client(
        'ec2',
        region_name=_region
    )
    res = client.describe_instances(
        InstanceIds = [_id]
    )
    return res[0]['Instances'][0]['PrivateDnsName']

def zbx_get_host(host_name):
    return zapi.host.get({
        'selectInterfaces': 'extend',
        'selectInventory': 'extend',
        'filter': {'host': host_name}
    })[0]

def zbx_enable_host(host_id):
    zapi.host.update({'hostid': host_id, 'status': 0})

def zbx_disable_host(host_id):
    zapi.host.update({'hostid': host_id, 'status': 1})

def lambda_handler(event, context):
    print("type = " + event['detail-type'])
    print("time = " + event['time'])
    print("state = " + event['detail']['state'])
    print("Done")
    host_name = aws_get_instance_info(event['detail']['instance-id'], event['region'])
    host = zbx_get_host(host_name)
    if event['detail']['state'] == 'running':
        if int(host['status']) == 1:
            print("Enabling host...")
            zbx_enable_host(host['hostid'])
    elif event['detail']['state'] == 'terminated':
        if int(host['status']) == 0:
            print("Disabling host...")
            zbx_disable_host(host['hostid'])
    return event['detail']['state']  # Echo back the first key value
    #raise Exception('Something went wrong')

