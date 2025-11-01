from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = None

    def human_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.human_delay(0.5, 1.2)

    def click_with_human_behavior(self, element):
        from selenium.webdriver.common.action_chains import ActionChains
        self.actions = ActionChains(self.driver)
        offset_x = random.randint(-8, 8)
        offset_y = random.randint(-5, 5)
        self.actions.move_to_element_with_offset(element, offset_x, offset_y)
        self.actions.pause(random.uniform(0.4, 1.0))
        self.actions.click().perform()
        self.human_delay(1.0, 2.5)

    def wait_for_url_contains(self, text, timeout=25):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: text in d.current_url
            )
            return True
        except TimeoutException:
            return False
        
    def is_perimeterx_present(self):
        """Detecta si PerimeterX está bloqueando (iframe o contenedor)"""
        selectors = [
            ".px-captcha-container",
            "iframe[title*='verificación']",
            "iframe[src*='perimeterx']",
            "div[id*='px']"
        ]
        return any(self.driver.find_elements(By.CSS_SELECTOR, sel) for sel in selectors)

    def handle_perimeterx(self):
        """Resuelve PerimeterX si aparece. Se puede llamar en cualquier punto."""
        if self.is_perimeterx_present():
            print("PERIMETERX DETECTADO! Resuelve manualmente...")
            self.driver.save_screenshot("perimeterx_detected.png")
            input("Presiona ENTER cuando desaparezca el desafío...")
            self.human_delay(2, 4)  # Espera estabilización
            return True
        return False
    
    def click_first_banner(self):
        banner = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'section[data-dca-id="M:164C43B0BC"] img#hero_1'))
        )
        self.scroll_to_element(banner)
        self.click_with_human_behavior(banner)
        print("Clic en el primer banner realizado.")