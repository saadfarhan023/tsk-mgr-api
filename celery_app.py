from celery import Celery

celery = Celery(
  "tsk-mgr-api",
  broker="redis://localhost:6379/0",
  backend="redis://localhost:6379/0",
  include=["tasks.jobs"]
)

celery.conf.task_track_started = True
