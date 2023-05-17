import grpc
import monitoreo_pb2
import monitoreo_pb2_grpc
from concurrent import futures
import time

HOST = '[::]:8080'

global capacidad
capacidad = 0

class monitoreo(monitoreo_pb2_grpc.monitoreoServicer):    
  def vigilancia(self, request, context):
        i = capacidad
        return monitoreo_pb2.EasyRequest(package= str(i))


def increase_number_every_second(number):  
  number = number + 1
  return number
      

def serve():
  global capacidad
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  monitoreo_pb2_grpc.add_monitoreoServicer_to_server(monitoreo(), server)
  server.add_insecure_port('[::]:8080')
  print("Service is running... ")
  server.start()
  capacidad_cpu = 0
  while True:
          capacidad_cpu = increase_number_every_second(capacidad_cpu)
          capacidad = capacidad_cpu
          print(capacidad)
          time.sleep(1)
  server.wait_for_termination()
  
  
  

if __name__ == "__main__":
        serve()
        
        