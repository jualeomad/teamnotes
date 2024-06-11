bind = "0.0.0.0:8000"  # Dirección y puerto en el que Gunicorn escuchará las conexiones
workers = 3  # Número de trabajadores para manejar las solicitudes
timeout = 30  # Tiempo máximo en segundos que un trabajador puede esperar una nueva solicitud
loglevel = "info"  # Nivel de registro de Gunicorn
