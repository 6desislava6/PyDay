from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()


def my_job(text):
    print(text)

# тук добавя всички аларми, които е прочел от pickle file-а
sched.add_job(my_job, 'date', run_date=datetime.now(), args=['text'])
sched.start()

# този процес се пуска във фонов режим, а когато получи нови данни за алармите, се спира и всички аларми се зареждат наново
