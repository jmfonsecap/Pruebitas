import datetime

tiempo_actual = datetime.datetime.now()#formato datetime
tiemposegundos = datetime.datetime.strptime("tiempo_actual", "%Y/%m/%d %H:%M:%S:%ms").timestamp()
tiempostring = tiempo_actual.strftime("%Y%m%d%H%M%S").timestamp()#formato string
tiempoint = float("tiempostring")

print (str("tiemposegundos"))