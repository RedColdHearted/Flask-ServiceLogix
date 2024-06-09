import unittest
from flask_login import current_user, logout_user
from app import create_app, db, bcrypt
from app.models import User, RepairRequest
from app.schemas import RepairRequestStatus


class UserLoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание тестового клиента и инициализация базы данных (один раз для всего класса)"""
        cls.app = create_app('config.TestingConfig')  # Предполагаем, что у вас есть конфигурация 'testing'
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Очистка базы данных после выполнения всех тестов"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Создание тестовых пользователей перед каждым тестом"""
        self.create_test_users()
        self.create_repair_requests()
        self.client = self.app.test_client()  # Генерируем новый клиент для каждого теста

    def tearDown(self):
        """Удаление данных тестового пользователя после каждого теста"""
        db.session.remove()
        db.drop_all()
        db.create_all()

    def create_test_users(self):
        """Создание пользователей для тестирования"""
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        self.repairman = User(username='repairman', email='repairman@example.com', password_hash=hashed_password, is_repairman=True)
        self.admin = User(username='adminuser', email='admin@example.com', password_hash=hashed_password, is_admin=True)
        db.session.add(self.repairman)
        db.session.add(self.admin)
        db.session.commit()

    def create_repair_requests(self):
        """Создание заявок на ремонт"""
        self.repair_request1 = RepairRequest(
            device_type='test',
            device_model='test',
            issue_description='test',
            client_name='test',
            client_phone='123',
            current_master_id=self.repairman.id
        )
        db.session.add(self.repair_request1)
        db.session.commit()

    def login_as_user(self, username, password):
        """Логин под определенным пользователем"""
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def test_login_and_access_profile_as_repairman(self):
        """Тест для входа и доступа к профилю под ремонтником"""
        with self.client:
            response = self.login_as_user('repairman', 'testpassword')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'repairman')
            profile_response = self.client.get('/profile')
            self.assertEqual(profile_response.status_code, 200)
            logout_user()  # Разлогиниваемся после теста

    def test_login_and_access_profile_as_admin(self):
        """Тест для входа и доступа к профилю под администратором"""
        with self.client:
            response = self.login_as_user('adminuser', 'testpassword')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'adminuser')
            profile_response = self.client.get('/profile')
            self.assertEqual(profile_response.status_code, 200)
            logout_user()  # Разлогиниваемся после теста

    def test_access_to_home(self):
        """Тест доступа к домашней странице"""
        with self.client:
            home_response = self.client.get('/')
            self.assertEqual(home_response.status_code, 200)

    def test_no_login_access(self):
        """Тест доступа к ulr'ам без логина"""
        with self.client:
            profile_url = '/profile'
            info_url = '/profile/info-request/' + str(self.repair_request1.id)
            edit_url = '/profile/edit-request/' + str(self.repair_request1.id)
            complete_url = '/profile/complete-request/' + str(self.repair_request1.id)
            search_url = '/profile/search'
            for url in (profile_url, info_url, edit_url, complete_url, search_url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_repairman_access_to_admin(self):
        """Тест отказа в доступе к админ странице ремонтнику"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'repairman')
            admin_redirect_response = self.client.get('/admin')
            admin_response = self.client.get('/admin/')
            self.assertEqual(admin_redirect_response.status_code, 308)
            self.assertEqual(admin_response.status_code, 404)
            logout_user()  # Разлогиниваемся после теста

    def test_create_repair_request(self):
        """Тест создания заявки"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            url = '/profile/create-request'
            form_data = {
                'device_type': 'Баджаджо',
                'device_model': 'Баджаджо',
                'issue_description': 'Баджаджо',
                'client_name': 'Баджаджо Баджаджо',
                'status': RepairRequestStatus['NEW'],
                'master_comment': 'Баджаджо',
                'is_active': True,
                'current_master': self.repairman.id
            }
            repair_request_response = self.client.post(url, data=form_data, follow_redirects=True)
            self.assertEqual(repair_request_response.status_code, 200)
            logout_user()


    def test_get_repair_request(self):
        """Тест доступа к странице заявки"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            url = '/profile/info-request/' + str(self.repair_request1.id)
            repair_request_response = self.client.get(url)
            self.assertEqual(repair_request_response.status_code, 200)
            logout_user()  # Разлогиниваемся после теста

    def test_complete_repair_request(self):
        """Тест доступа к завершению заявки"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            complete_url = '/profile/complete-request/' + str(self.repair_request1.id)
            repair_request_response = self.client.post(complete_url)
            self.assertEqual(repair_request_response.status_code, 302)
            edit_url = '/profile/edit-request/' + str(self.repair_request1.id)
            repair_request_response = self.client.post(edit_url)
            self.assertEqual(repair_request_response.status_code, 404)
            logout_user()

    def test_edit_repair_request(self):
        """Тест доступа к изменению заявки"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            url = '/profile/edit-request/' + str(self.repair_request1.id)
            form_data = {
                'device_type': 'Смартфон',
                'device_model': 'iPhone X',
                'issue_description': 'Экран не работает',
                'client_name': 'Иван Иванов',
                'status': RepairRequestStatus['NEW'],
                'master_comment': 'Проблема с экраном',
                'is_active': True,
                'current_master': self.repairman.id
            }
            repair_request_response = self.client.post(url, data=form_data, follow_redirects=True)
            self.assertEqual(repair_request_response.status_code, 200)
            logout_user()

    def test_repair_request_search_result(self):
        """Тест поиска заявки по номеру телефона"""
        with self.client:
            self.login_as_user('repairman', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            url = '/profile/search'
            form_data1 = {
                'client_phone': self.repair_request1.client_phone
            }
            repair_request_response1 = self.client.post(url, data=form_data1, follow_redirects=True)
            self.assertEqual(repair_request_response1.status_code, 200)
            form_data2 = {
                'client_phone': 000,
            }
            repair_request_response2 = self.client.post(url, data=form_data2, follow_redirects=True)
            self.assertEqual(repair_request_response2.status_code, 200)
            logout_user()

    def test_admin_access_to_admin(self):
        """Тест доступа к админ странице администратором"""
        with self.client:

            self.login_as_user('adminuser', 'testpassword')
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'adminuser')
            admin_redirect_response = self.client.get('/admin')
            admin_response = self.client.get('/admin/')
            self.assertEqual(admin_redirect_response.status_code, 308)
            self.assertEqual(admin_response.status_code, 200)
            logout_user()  # Разлогиниваемся после теста


if __name__ == '__main__':
    unittest.main()
