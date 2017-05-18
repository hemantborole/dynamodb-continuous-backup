#!/usr/bin/env python

'''
Module which gives customers the ability to provision existing DynamoDB tables for continuous backup
'''
import sys

# add the lib directory to the path
sys.path.append('lib')

import dynamo_continuous_backup
import boto3
import argparse
import os
import hjson

REGION_KEY = 'AWS_REGION'
dynamo_client = None


global session
if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("--region", dest='region', action='store', required=False, help="Enter the destination region")
    parser.add_argument("--profile", required=True, help="Profile name for AWS Credentials")    
    parser.add_argument("--table-list", required=True, help="List of tables to whitelist")    
    args = parser.parse_args()

def init():
    try:
        #current_region = os.environ[REGION_KEY]
        current_region = args.region
        os.environ[REGION_KEY] = args.region
    
        if current_region == None or current_region == '':
            raise KeyError
    except KeyError:
        raise Exception("Unable to resolve environment variable %s" % REGION_KEY)
    
    global dynamo_client
    
    session = boto3.Session(profile_name = args.profile, region_name = args.region)
    dynamo_client = session.client('dynamodb', region_name=current_region)
    
    
def resolve_table_list(config_file):
    # determine if there was a config file with a whitelist, or if we are provisioning all existing tables
    if config_file != None:
        print "Building Table List for Processing from %s" % (config_file)
        config = hjson.load(open(config_file, 'r'))

    table_list = []
    if config == None or config == [] or config["provisionAll"] == True:
        last_table_evaluated = str(None)
        while last_table_evaluated != None or len(table_list) == 0:
            list_table_result = dynamo_client.list_tables(ExclusiveStartTableName=last_table_evaluated)
            
            for x in list_table_result['TableNames']:
                table_list.append(x) 
                
            if "LastEvaluatedTableName" in list_table_result:
                last_table_evaluated = list_table_result['LastEvaluatedTableName']
            else:
                break
                
    else:
        table_list = config["tableNames"]
        
    return table_list

        
def provision_tables(table_list):
    for x in table_list:
        try:
            dynamo_continuous_backup.configure_table(x)
        except Exception as e:
            print "Exception while provisioning table %s" % (x)
            print e
            print "Proceeding..."


def deprovision_tables(table_list):
    for x in table_list:
        try:
            dynamo_continuous_backup.deprovision_table(x)
        except Exception as e:
            print "Exception while deprovisioning table %s" % (x)
            print e
            print "Proceeding..."

   
def deprovision(table_whitelist):
    init()
    
    table_list = resolve_table_list(table_whitelist)
    
    dynamo_continuous_backup.init(None)
        
    deprovision_tables(table_list)
        
        
#def provision(table_whitelist):
def provision():
    table_whitelist = args.table_list
    init()
    
    table_list = resolve_table_list(table_whitelist)
    
    dynamo_continuous_backup.init(None)
        
    provision_tables(table_list)


provision()
