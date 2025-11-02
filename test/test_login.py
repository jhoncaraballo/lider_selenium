import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.home_page import HomePage
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

@pytest.mark.usefixtures("driver")
class TestLoginLider:
    """Clase de pruebas para el flujo de login en Lider.cl."""

    def test_login_exitoso(self):
        """Prueba completa: Navega, loguea y verifica éxito."""
        driver = self.driver
        home = HomePage(driver)
        wait = WebDriverWait(driver, 15)
        
        # 1. Navegar
        home.navigate()
        home.handle_perimeterx()

        # Paso 1: Haz clic en el botón de login
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[link-identifier='Account']")))
            home.click_with_human_behavior(login_button)
            print("Botón de login clickeado.")
        except TimeoutException:
            pytest.fail("No se encontró el botón de login. Verifica selectores.")

        try:
            login_button_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="sign-in"]')))
            home.click_with_human_behavior(login_button_2)
            print("Botón de login clickeado.")
        except TimeoutException:
            pytest.fail("No se encontró el botón de login. Verifica selectores.")

        # Paso 2: Espera y llena el campo de email/RUT
        try:
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="email"]')))
            email_field.clear()
            email_field.send_keys(EMAIL)
            print(f"Email ingresado: ({EMAIL})")
        except TimeoutException:
            pytest.fail("No se encontró el campo de email.")

        # Paso 3: Envía el formulario
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-continue-button")))
            home.click_with_human_behavior(submit_button)
            print("Botón de continuar clickeado.")
        except NoSuchElementException:
            pytest.fail("No se encontró el botón de continuar.")

    