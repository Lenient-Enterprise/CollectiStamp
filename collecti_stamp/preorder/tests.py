from django.test import TestCase,BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
class UserManagementTestCase(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

        self.username = 'alesanfel'
        self.email = 'alex.0002002@gmail.com'
        self.password = 'Hola$1234'

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        
    def test_edit(self):
        hola=""
