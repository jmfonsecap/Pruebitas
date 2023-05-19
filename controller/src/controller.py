import logging
import boto3
import boto3.session
from concurrent import futures
import json
import time
import grpc
import controller_pb2
import controller_pb2_grpc

HOST = '[::]:8080'
my_session = boto3.session.Session()

archivo = open('archivo.txt', 'w')

oldInstances=[]
newInstances=[]

resource_ec2 = boto3.client("ec2", 
                            aws_access_key_id="ASIATJHWQLIKI4AAH3YS",
                            aws_secret_access_key="9ww0Y0cOXkZCPm4BIf+cz/bOLpMhW6Kshv96u3T0",
                            aws_session_token="FwoGZXIvYXdzEFgaDC9zjHy4e0CV0F4y6SLIAfvt6NPHnj0jmF2QTadQF94MKpovV3wDH/+18Sshs6atiShY4F1v2GUzFPZqO+GjyUmjhbbbYJt8+bbqduVGvfybymE57+QyD2sSQnYKqiArDfV9eAubijoXIxXVcKIu+Sh8boddxt4giubSCSQTJ6PQz9MtdYzjKe3fjCmyWFCc1a31VlnBnl0OJPUQGmvO7d/2qGmZwJiNGnaYXjJueJbaNuisyzuguzjK1Z4cVf9Q0UjX7Qo1redmQurNrMUU54xjKS6IJSjKKM2jnKMGMi15shNuUlaaC1mIRnVFNIg7LIsmCGt/GakdSAp7jYydx7sZKmvBZKV1HxZp8uk=",
                            region_name='us-east-1')

lt = {
    'LaunchTemplateId': 'lt-0b369b2430457df2b',
}

def create_ec2_instance():
    get_old_instances()
    try:
        global archivo
        archivo.write("Creating EC2 instance")
        print ("Creating EC2 instance")
        resource_ec2.run_instances(
            LaunchTemplate=lt,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="TeleKey")
        time.sleep(1)
        get_new_instance()
        
    except Exception as e:
        print(e)

def get_old_instances():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] not in oldInstances:
                    oldInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_new_instance():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                actualid=instance['InstanceId']
                if actualid not in oldInstances:
                    newInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_ipv4(instance_id):
    response = resource_ec2.describe_instances(InstanceIds=[instance_id])
    ipv4_publico = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return ipv4_publico

def terminate_ec2_instance(instance_id):
    try:
        global archivo
        archivo.write("Terminate EC2 instance")
        print("Terminate EC2 instance")
        util=resource_ec2.terminate_instances(InstanceIds=[instance_id])
        archivo.write(util)
        print(util)
        newInstances.remove(instance_id)
        return "Instancia " + instance_id+ " terminada"
    except Exception as e:
        print(e)
        return 

def minimum_instances():
    if len(newInstances)<2:
        while len(newInstances)<2: 
            create_ec2_instance()
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def Ping(ipv4_publica):
    with grpc.insecure_channel(ipv4_publica+":8080") as channel:
        stub = controller_pb2_grpc.controllerStub(channel)
        response = stub.Ping(controller_pb2.Nada())
    return response
def serve():
    global archivo
    starttime = time.time()
    minimum_instances()
    print("waiting for instances to launch")
    archivo.write("waiting for instances to launch")
    time.sleep(180)
    while True:
        minimum_instances()
        for instance in newInstances:
            ip = get_ipv4(instance)
            try:
                response= Ping(ip)
                if response.status_code==0:
                    print(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                    archivo.write(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                    if response.cpu_usage>50 and response.cpu_usage<80:
                        if len(newInstances)<4:
                            create_ec2_instance()
                    elif response.cpu_usage>80:
                        terminate_ec2_instance(instance)
            except:
                print(ip+" esta prendiendo")
                archivo.write(ip+" esta prendiendo")
            
        time.sleep(30.0-((time.time() - starttime)%30.0))

def serve2():
    starttime = time.time()
    while True:
        ip ="3.93.20.58"
        try:
            response= Ping(ip)
            if response.status_code==0:
                print(ip+" esta activa y la ocupacion de su cpu es de "+ str(response.cpu_usage))
                
                if response.cpu_usage>50 and len(newInstances)<4 and response.cpu_usage<80:
                    #create_ec2_instance()
                    print("hola")
                elif response.cpu_usage>80:
                    #terminate_ec2_instance(instance)
                    print("hola")
        except Exception as e:
            print(e)
        
        time.sleep(5.0-((time.time() - starttime)%5.0))        
if __name__ == '__main__':
    logging.basicConfig()
    serve()
