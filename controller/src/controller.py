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


oldInstances=[]
newInstances=[]

resource_ec2 = boto3.client("ec2", 
                            aws_access_key_id='ASIA5KF4RYNQ5REV6EXA',
                            aws_secret_access_key='eYNElknn1U3ErrhnNtqNB9zitP7v8U2oRI6dutsJ',
                            aws_session_token='FwoGZXIvYXdzEO3//////////wEaDDSTi8EZMptRjsmBXyLHAVWzJZIquyW7ajnaXCD8PkHizqdc90pUg8rekG5ZFDfSpDq+gVHP4YrxuH+tdkEsAxGKUUTaAWfsr7Qo7G6Y9wo0FjGkUw+Slw3cvutJfRSwrajIMOOWbUqoTLphJkniAuwQ7zWIVobfJf/y7YQOnt4SmtNmprBUAutK9Rh89awef95QKDtC0zHH1etSqTh61+1+fQTFXtRLXSamCnnl1MAYduEjEcJWtVTNigBQ0kRZ3nbkLnY28je0qXZ8cbrSwMkzJN0s+JUo3fiEowYyLZA1Cr+fhqd88qv9tr+9e13cLwMz75evyIvh8HcFLV3VFuP7D+V/gnM2oRso4Q==',
                            region_name='us-east-1')

def create_ec2_instance():
    get_old_instances()
    try:
        print ("Creating EC2 instance")
        resource_ec2.run_instances(
            ImageId="ami-0242669d1b95f4db5",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="Andres")
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
    print(f"La dirección IPv4 pública de la instancia {instance_id} es {ipv4_publico}")
    return ipv4_publico

def terminate_ec2_instance(instance_id):
    try:
        print ("Terminate EC2 instance")
        print(resource_ec2.terminate_instances(InstanceIds=[instance_id]))
        newInstances.remove(instance_id)
        return "Instacia " + instance_id+ " terminada"
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
            
if __name__ == "_main_":
    starttime = time.time()
    while True:
        minimum_instances()
        for instance in newInstances:
            ip = get_ipv4(instance)
            response= Ping(ip)
            if response.status_code==0:
                print(ip+" esta activa y la ocupacion de su cpu es de "+ response.cpu_usage)
                if response.cpu_usage>50 and len(newInstances)<4 :
                    create_ec2_instance()
                elif response.cpu_usage>80:
                    terminate_ec2_instance(instance)
            elif response.status_coded==1:
                print(ip+" esta caida" )
        time.sleep(30.0-((time.time() - starttime) % 30.0))