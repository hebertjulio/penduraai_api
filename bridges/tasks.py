from celery import shared_task


@shared_task(bind=True)
def push_notification(self, group, message):
    pass
