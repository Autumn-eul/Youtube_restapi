from django.test import SimpleTestCase
from unittest.mock import patch
from django.core.management import call_command

from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OperationalError

@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandsTests(SimpleTestCase):

    # DB 가 준비되었을 때 wait_for_db 잘 동작하는지 체크하는 함수
    def test_wait_for_db_ready(self, patched_getitem):
        patched_getitem.return_value = True

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 1)

    # DB 연결에 오류가 발생했다 가정하고 테스트
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_getitem):
        patched_getitem.side_effect = [Psycopg2OperationalError] + \
            [OperationalError] * 5 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 7)

# docker-compose run --rm app sh -c "python manage.py test core"