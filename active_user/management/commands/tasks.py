from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()


        sched.start()