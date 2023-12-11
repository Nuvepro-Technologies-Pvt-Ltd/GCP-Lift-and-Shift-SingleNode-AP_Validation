from result_output import *
import sys
import json
import importlib.util
import urllib.request
from google.oauth2 import service_account
from googleapiclient import discovery
from pprint import pprint
from google.cloud import logging

class Activity():

    def testcase_check_VMName(self,test_object,credentials,project_id):
        testcase_description="Check VM instance name"
        expected_result='co-workspace'
        zone = "asia-south1-c"
        try:
            is_present = False
            actual = 'Instance name is not '+ expected_result
            service = discovery.build('compute', 'v1', credentials=credentials)
            try:
                request = service.instances().list(project=project_id, zone=zone)
                response = request.execute()
                if 'items' in response:
                    instances = response['items']
                    for instance in instances:
                        if instance['name']== expected_result:
                            is_present=True
                            actual=expected_result
                            break
                        else:
                            actual= instance['name']
                else:
                    pass

            except Exception as e:
                is_present = False
            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"No Comment"," Congrats! You have done it right!") 
            else:
                test_object.update_result(0,expected_result,actual,"Check instance name","https://cloud.google.com/compute/docs/instances/create-start-instance")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_instance_name"]=str(e)                

            
def start_tests(credentials, project_id, args):

    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules[ "result_output"])
    
    test_object=ResultOutput(args,Activity)
    challenge_test=Activity()
    challenge_test.testcase_check_VMName(test_object,credentials,project_id)
    #challenge_test.testcase_check_VMStatus(test_object,credentials,project_id)

    json.dumps(test_object.result_final(),indent=4)
    return test_object.result_final()

