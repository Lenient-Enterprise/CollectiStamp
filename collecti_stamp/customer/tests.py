from django.contrib.auth.tokens import default_token_generator
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from selenium import webdriver

from customer.models import User
from selenium.webdriver.common.by import By


# Create your tests here.
class TestRegister(StaticLiveServerTestCase):
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


    def test_register(self):
        self.driver.get(self.live_server_url + '/base/')

        self.driver.set_window_size(1918, 858)
        self.driver.find_element(By.LINK_TEXT, "Registrarse").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.username)
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys(self.email)
        self.driver.find_element(By.ID, "id_password1").click()
        self.driver.find_element(By.ID, "id_password1").send_keys(self.password)
        self.driver.find_element(By.ID, "id_password2").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)
        user.delete()

    def test_validate(self):
        User.objects.create(username=self.username, email=self.email, password=self.password)
        user = User.objects.get(username=self.username)
        token = default_token_generator.make_token(user)

        # Generar la URL de verificación por correo electrónico
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = reverse('verify_email', args=[uid, token])
        self.driver.get(self.live_server_url + verify_url)
        user = User.objects.get(username=self.username)
        self.assertEqual(user.email_verified, True)

class RequestPasswordResetViewTests(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

        self.username = 'alesanfel'
        self.email = 'alex.0002002@gmail.com'
        self.password = 'Hola$1234'
        self.new_password = 'Hola$12345'
        self.user = User.objects.create(username=self.username, email=self.email, password=self.password, email_verified=True)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.user.delete()

    def test_request_password_reset(self):
        self.driver.get(f"{self.live_server_url}/customer/password-reset/")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys(self.email)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        self.driver.close()

    def test_change_password(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.driver.get(f"{self.live_server_url}/customer/change-password/{uid}/{token}/")
        self.driver.set_window_size(1850, 1016)
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys(self.new_password)
        self.driver.find_element(By.ID, "id_confirm_password").click()
        self.driver.find_element(By.ID, "id_confirm_password").send_keys(self.new_password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.user = User.objects.get(username=self.username)
        self.assertTrue(self.user.check_password(self.new_password))
        self.assertTrue(self.driver.current_url == f"{self.live_server_url}/base/?message=Contrase%C3%B1a%20cambiada&status=Success")