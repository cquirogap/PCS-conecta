from apscheduler.schedulers.blocking import BlockingScheduler
import os

def ejecutar_tarea():
    print("Ejecutando tarea Django desde apscheduler")
    os.system('source /home/pcsenv/bin/activate && cd /home/pcs-conecta/pcs && python manage.py tarea')

sched = BlockingScheduler()
sched.add_job(ejecutar_tarea, 'cron', hour=14, minute=0)  # Ejecutar todos los dias a las 14:00
sched.start()