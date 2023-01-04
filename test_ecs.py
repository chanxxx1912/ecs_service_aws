import boto3
import ecs
from ecs import ecs_aws
from moto import mock_ecs,mock_ec2
ACCOUNT_ID = 1234567890
import json
from moto.ec2 import utils as ec2_utils


@mock_ec2
@mock_ecs
def test_list_tasks():
    conn  = boto3.client("ecs", region_name="us-east-1")
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    _ = conn.create_cluster()

    test_instance = ec2.create_instances(
        ImageId='ami-12c6146b', MinCount=1, MaxCount=1
    )[0]
    instance_id_document = json.dumps(
        ec2_utils.generate_instance_identity_document(test_instance)
    )
    _ = conn.register_container_instance(
        instanceIdentityDocument=instance_id_document
    )
    container_instances = conn.list_container_instances()
    container_instance_id = container_instances["containerInstanceArns"][0].split("/")[-1]
    _ = conn.register_task_definition(
        family="default",
        containerDefinitions=[
            {
                "name": "hello_world",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "essential": True,
                "environment": [
                    {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                ],
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )
    _ = conn.start_task(
        taskDefinition="default",
        overrides={},
        containerInstances=[container_instance_id],
        startedBy="foo",
    )
    tasks_arns = [
        task["taskArn"]
        for task in conn.run_task(
            cluster="default",
            overrides={},
            taskDefinition="default",
            count=2,
            startedBy="moto",
        )["tasks"]
    ]
    _  = conn.describe_tasks(cluster="default", tasks=tasks_arns)
    
    conn  = boto3.client("ecs", region_name="us-east-1")
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    _ = conn.create_cluster(clusterName="harna")

    test_instance = ec2.create_instances(
        ImageId='ami-12c6146b', MinCount=1, MaxCount=1
    )[0]
    instance_id_document = json.dumps(
        ec2_utils.generate_instance_identity_document(test_instance)
    )
    _ = conn.register_container_instance(
        instanceIdentityDocument=instance_id_document,cluster="harna"
    )
    container_instances = conn.list_container_instances()
    container_instance_id = container_instances["containerInstanceArns"][0].split("/")[-1]
    _ = conn.register_task_definition(
        family="harna",
        containerDefinitions=[
            {
                "name": "hello_world",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "essential": True,
                "environment": [
                    {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                ],
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )
    _ = conn.start_task(
        taskDefinition="harna",
        overrides={},
        containerInstances=[container_instance_id],
        startedBy="foo",
    )
    tasks_arns = [
        task["taskArn"]
        for task in conn.run_task(
            cluster="harna",
            overrides={},
            taskDefinition="harna",
            count=2,
            startedBy="moto",
        )["tasks"]
    ]
    _  = conn.describe_tasks(cluster="harna", tasks=tasks_arns)
    
    
    
   
  
    ecs_aws()