from django.core.management.base import BaseCommand, CommandError
from etl.models import FactTable, ETLHistory
from workinterface.models import Answers
from django.db import connection
from itertools import chain


class Command(BaseCommand):
    help = 'Updates the Fact Table'

    def handle(self, *args, **options):
        # First try to get the latest update id
        try:
            latest_record = ETLHistory.objects.latest('timestamp')
            sql_fetch_data = """SELECT
              workinterface_job.task_title,
              crowdcur_taskfeaturesmodel.feature->>'requester' AS task_requester,
              accounts_user.username AS worker,
              workinterface_job.task_payment,
              crowdcur_workertaskhistorymodel.time_it_took,              
              accounts_user.age,
              accounts_user.nationality,
              accounts_user.education,
              EXTRACT(YEAR FROM crowdcur_workertaskhistorymodel.timestamp) AS year,
              EXTRACT(MONTH FROM crowdcur_workertaskhistorymodel.timestamp) AS month,
              EXTRACT(Day FROM crowdcur_workertaskhistorymodel.timestamp) AS day,
              to_char(crowdcur_workertaskhistorymodel.timestamp,'DAY') as day_of_week,
              EXTRACT(HOUR FROM crowdcur_workertaskhistorymodel.timestamp) as time_of_day
            FROM
              accounts_user,
              workinterface_answers,
              workinterface_task,
              workinterface_job,
              crowdcur_workertaskhistorymodel,
              crowdcur_taskfeaturesmodel
            WHERE
              workinterface_task.id = workinterface_answers.task_id
              and workinterface_task.task_type_id = workinterface_job.id
              and workinterface_task.id = crowdcur_workertaskhistorymodel.task_id
              and accounts_user.id = workinterface_answers.worker_id
              and accounts_user.id = crowdcur_workertaskhistorymodel.worker_id
              and crowdcur_workertaskhistorymodel.successful = true
              and crowdcur_taskfeaturesmodel.task_id = workinterface_task.id
              and workinterface_answers.id > %s
            """

            with connection.cursor() as cursor:
                cursor.execute(sql_fetch_data,[latest_record.last_inserted_id])
                data = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

        except ETLHistory.DoesNotExist:
            latest_id = Answers.objects.order_by('pk').last()
            if latest_id is None:
                return

            sql_fetch_data = """SELECT
              workinterface_job.task_title,
              crowdcur_taskfeaturesmodel.feature->>'requester' AS task_requester,
              accounts_user.username AS worker,
              workinterface_job.task_payment,
              crowdcur_workertaskhistorymodel.time_it_took,              
              accounts_user.age,
              accounts_user.nationality,
              accounts_user.education,
              EXTRACT(YEAR FROM crowdcur_workertaskhistorymodel.timestamp) AS year,
              EXTRACT(MONTH FROM crowdcur_workertaskhistorymodel.timestamp) AS month,
              EXTRACT(Day FROM crowdcur_workertaskhistorymodel.timestamp) AS day,
              to_char(crowdcur_workertaskhistorymodel.timestamp,'DAY') as day_of_week,
              EXTRACT(HOUR FROM crowdcur_workertaskhistorymodel.timestamp) as time_of_day
            FROM
              accounts_user,
              workinterface_answers,
              workinterface_task,
              workinterface_job,
              crowdcur_workertaskhistorymodel,
              crowdcur_taskfeaturesmodel
            WHERE
              workinterface_task.id = workinterface_answers.task_id
              and workinterface_task.task_type_id = workinterface_job.id
              and workinterface_task.id = crowdcur_workertaskhistorymodel.task_id
              and accounts_user.id = workinterface_answers.worker_id
              and accounts_user.id = crowdcur_workertaskhistorymodel.worker_id
              and crowdcur_workertaskhistorymodel.successful = true
              and crowdcur_taskfeaturesmodel.task_id = workinterface_task.id
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_fetch_data)
                data = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
        if len(data) > 0:
            latest_id = Answers.objects.order_by('pk').last().id
            item_count = len(data)
            ETLHistory.objects.create(last_inserted_id=latest_id, number_of_records=item_count)

            sql = "INSERT INTO etl_facttable ({0}) VALUES {1}".format(
                ', '.join(columns), ','.join(['({})'.format(', '.join(['%s'] * len(columns)))] * item_count))
            with connection.cursor() as cursor:
                params = list(chain.from_iterable(data))
                cursor.execute(sql,params)
            self.stdout.write(self.style.SUCCESS("%s new records added!"%item_count))
        else:
            self.stdout.write(self.style.ERROR("No new record found!"))
