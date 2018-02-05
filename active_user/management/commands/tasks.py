from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()

        from active_user.models import madadjoo, hamyar, sponsership
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        @sched.scheduled_job('interval', days=60)
        def timed_job():
            for target_hamyar in hamyar.objects.all():
                message = target_hamyar.first_name + " " + target_hamyar.last_name + " عزیز شرح وضعیت تحصیلی مددجویان تحت حمایت شما در زیر آمده است"
                corr_madadjoos_ids = sponsership.objects.filter(hamyar=target_hamyar).values('madadjoo_id')
                corr_madadjoos = madadjoo.objects.filter(active_user_ptr__in=corr_madadjoos_ids)

                for target_madadjoo in corr_madadjoos:
                    message += '\n' + target_madadjoo.first_name + " " + target_madadjoo.last_name + ": " + target_madadjoo.edu_status

                print("here")

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('childf2018', 'childF20182018')
                msg = MIMEMultipart()
                msg['From'] = 'childf2018@gmail.com'
                msg['To'] = target_hamyar.email
                msg['Subject'] = 'گزارش وضعیت تحصیلی مددجویان تحت حمایت'
                msg.attach(MIMEText(message, 'plain'))
                server.send_message(msg)
                server.quit()

        sched.start()
