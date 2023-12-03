from celery import shared_task
from celery import Celery
from celery.schedules import crontab



@shared_task
def test():
    print("test de prueba")
    return "test de prueba cons"