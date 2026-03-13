from src.core.celery_app import celery_app
import logging


@celery_app.task(name="collect_prices", max_retries=3)
def collect_prices():
    logging.log(logging.INFO, "Test")
