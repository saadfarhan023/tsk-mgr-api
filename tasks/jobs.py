from celery_app import celery

@celery.task
def notify_task_created(task_id: int, title: str):
  print(f"[notify] Task {task_id} created: '{title}'")
  return {"task_id": task_id, "notified": True}
