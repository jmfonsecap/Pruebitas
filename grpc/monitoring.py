import grpc
import controller_pb2
import controller_pb2_grpc
from concurrent import futures
import time



global capacidad
capacidad = 0

class controller(controller_pb2_grpc.controllerServicer):    
  def Ping(self, request, context):
        i = capacidad
        return controller_pb2.Response(status_code= 0, cpu_usage=i)


def increase_number_every_second(number):  
  number = number + 1
  return number
      

def serve():
  global capacidad
  port ='8080'
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  controller_pb2_grpc.add_controllerServicer_to_server(controller(), server)
  server.add_insecure_port('[::]:' + port)
  print("Service is running... " +port)
  server.start()
  capacidad_cpu = 0
  while True:
          capacidad_cpu = increase_number_every_second(capacidad_cpu)
          capacidad = capacidad_cpu
          print(capacidad)
          time.sleep(10)
  server.wait_for_termination()
  
  
  

if __name__ == "__main__":
        serve()
        
        
