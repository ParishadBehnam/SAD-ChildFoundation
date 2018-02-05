from apscheduler.schedulers.blocking import BlockingScheduler
# from active_user.models import madadjoo, hamyar, sponsership
# from django.conf import settings

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    for target_hamyar in hamyar.objects.all():
        message = target_hamyar.first_name + " " + target_hamyar.last_name + " عزیز شرح وضعیت تحصیلی مددجویان تحت حمایت شما در زیر آمده است"
        corr_madadjoos_ids = sponsership.objects.filter(hamyar=target_hamyar).values('madadjoo_id')
        corr_madadjoos = madadjoo.objects.filter(active_user_ptr__in=corr_madadjoos_ids)

        for target_madadjoo in corr_madadjoos:
            message += '\n' + target_madadjoo.first_name + " " + target_madadjoo.lastname + ": " + target_madadjoo.edu_status

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

# settings.configure()
sched.start()