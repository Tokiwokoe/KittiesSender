from celery import Celery
from celery.schedules import crontab


app = Celery('bot')
app.config_from_object('bot.celeryconfig', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-cat-pic-every-hour': {
        'task': 'bot.tasks.send_catpic_task',
        'schedule': crontab(hour='8-21', minute='0'),
    },
}
