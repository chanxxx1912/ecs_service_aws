import boto3

def ecs_aws():
    client = boto3.client("ecs", region_name="us-east-1")
    paginator = client.get_paginator('list_clusters')
    
    response_iterator = paginator.paginate()
    for clusters_arn in response_iterator:
        
        for each_cluster_arn in clusters_arn['clusterArns']:
            #print(each_cluster_arn)
            
            task_list = client.list_tasks(
              cluster = (each_cluster_arn)
            )
            task_arn_inside_task_list =(task_list['taskArns'])

            for elements_in_task_list in task_arn_inside_task_list:
                task_arn = (elements_in_task_list)
                task_name = (elements_in_task_list.split('/')[1])
                task_id = (elements_in_task_list.split ('/')[2]) 
                
                describe_task =  client.describe_tasks(
                cluster = (each_cluster_arn),
                tasks =[
                    task_id
                ]
                )
                #print(describe_task )

                containers = []

                tasks = describe_task['tasks']
                #print(tasks)
                
                
        for task_details in tasks:
            containers = task_details['containers']
            task_definition_name  = task_details['taskDefinitionArn']
            print(task_definition_name)


            for container in containers:
                #Cluster Name

                str = (f"ClusterName = {each_cluster_arn.split('/')[1]}")
                dictionary = dict(subString.split("=") for subString in str.split(";"))
                print(str)



                #Task id or Name

                str1 = (f"TaskId/Name = {task_name}")
                dictionary1 = dict(subString.split("=") for subString in str1.split(";"))
            



                #Task Def id or name
                str2 = (f"TaskDefId/Name = {task_definition_name.split('/')[1]}")   
                dictionary2 = dict(subString.split("=") for subString in str2.split(";"))
               

                #Image name
                image = (container['name'])
                str3 = (f"ImageName = {image}")
                dictionary3 = dict(subString.split("=") for subString in str3.split(";"))
                #print(dictionary3)

                #Image tag
                image_tag = (container['image'])
                str4 = (f"ImageTag = {image_tag}")
                dictionary4 = dict(subString.split("=") for subString in str4.split(";"))
                #print(dictionary4)

                




       
      
    
                    