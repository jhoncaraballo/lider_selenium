from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HomePage(BasePage):
    # Selectores
    BTN_CATEGORIES = (By.CSS_SELECTOR, "[link-identifier='Departments']")
    PERIMETERX_IFRAME = (By.CSS_SELECTOR, ".px-captcha-container, iframe[title*='verificación']")
    FIRST_BANNER= (By.CSS_SELECTOR, "[link-identifier='Compra ahora']")

    def navigate(self):
        print("Navegando a https://www.lider.cl/inicio...")
        self.driver.get("https://www.lider.cl/inicio")
        self.human_delay(4, 7)
        self.handle_perimeterx()

    #def handle_perimeterx(self):
    #    if self.driver.find_elements(*self.PERIMETERX_IFRAME):
    #        print("PERIMETERX DETECTADO! Resuelve manualmente...")
    #        input("Presiona ENTER cuando desaparezca...")

    def open_categories_menu(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_CATEGORIES))
        self.scroll_to_element(btn)
        self.click_with_human_behavior(btn)
        print("Botón 'Categorías' clickeado (100% humano).")
        self.handle_perimeterx()

    def click_first_banner(self):
        banner = self.wait.until(EC.element_to_be_clickable(self.FIRST_BANNER))
        self.scroll_to_element(banner)
        self.click_with_human_behavior(banner)
        print("Click en el primer banner realizado.")
        self.handle_perimeterx()