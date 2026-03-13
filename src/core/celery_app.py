from celery import Celery

celery_app = Celery(
    "deribit_price_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["src.tasks.collect_prices"],
)

celery_app.conf.beat_schedule = {
    "collect-prices-every-minute": {"task": "collect_prices", "schedule": 60}
}

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
