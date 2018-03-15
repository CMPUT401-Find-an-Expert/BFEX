import os

from celery import Celery

BROKER_TYPE = "redis://"

CELERY_TASK_LIST = [
    "bfex.tasks",
]

def make_celery():
    # Configure Celery
    celery_broker = os.getenv("CELERY_BROKER", "localhost:6379")
    celery_backend = os.getenv("CELERY_BACKEND", "localhost:6379")
    
    celery_broker = BROKER_TYPE + celery_broker
    celery_backend = BROKER_TYPE + celery_backend
    
    print(celery_backend, celery_broker)
    celery = Celery("bfex_celery", broker=celery_broker, 
                    backend=celery_backend, includes=CELERY_TASK_LIST)

    celery.conf.update(
        CELERY_TASK_SERIALIZER = 'pickle',
        CELERY_RESULT_SERIALIZER = 'pickle',
        CELERY_ACCEPT_CONTENT = ['pickle']
    )

    return celery


celery_instance = make_celery()
