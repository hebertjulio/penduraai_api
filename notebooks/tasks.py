from celery import shared_task


@shared_task(bind=True)
def record_create(
        self, operation, value, note, merchant, attendant, signatary):
    print(operation, value, note, merchant, attendant, signatary)


@shared_task(bind=True)
def sheet_create(self, merchant, customer):
    print(merchant, customer)
