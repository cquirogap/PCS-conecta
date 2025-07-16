from apscheduler.schedulers.blocking import BlockingScheduler
import os

def ejecutar_tarea():
    print("🟢 Ejecutando tarea Django desde apscheduler")
    os.system('. /home/pcsenv/bin/activate && cd /home/pcs-conecta/pcs && python manage.py tarea')

sched = BlockingScheduler()

# Agregar las 3 ejecuciones diarias
sched.add_job(ejecutar_tarea, 'cron', hour=8, minute=0)
sched.add_job(ejecutar_tarea, 'cron', hour=12, minute=0)
sched.add_job(ejecutar_tarea, 'cron', hour=16, minute=0)
sched.add_job(ejecutar_tarea, 'cron', hour=20, minute=30)

sched.start()