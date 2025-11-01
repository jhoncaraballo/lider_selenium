from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import random

class CategoryMenuPage(BasePage):
    # Selectores principales
    MENU_VIEW_ALL = (By.CSS_SELECTOR, '[link-identifier="viewAllDepartment"]')
    BTN_CATEGORY = (By.CSS_SELECTOR, 'button[data-dca-name]')
    SUBMENU_CONTAINER = (By.CSS_SELECTOR, 'div[data-testid="category-menu"]')
    SUBCATEGORY_LINK = (By.CSS_SELECTOR, 'ul a.subcategory-item-link')

    def wait_for_menu(self):
        self.wait.until(EC.presence_of_element_located(self.MENU_VIEW_ALL))
        print("Menú desplegado.")

    def get_main_categories(self):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self.BTN_CATEGORY))
        categories = [
            btn for btn in buttons
            if btn.is_displayed() and btn.text.strip() and len(btn.text.strip()) > 2
        ]
        print(f"{len(categories)} categorías válidas encontradas:")
        for i, cat in enumerate(categories):
            print(f"  [{i+1}] {cat.text} → data-dca-name: {cat.get_attribute('data-dca-name')}")
        return categories

    def select_random_main_category(self, categories):
        category = random.choice(categories)
        name = category.text.strip()
        print(f"Seleccionando categoría principal: '{name}'")
        self.scroll_to_element(category)
        self.click_with_human_behavior(category)
        print(f"Click en '{name}' realizado.")
        self.human_delay(2.0, 4.0)
        return name

    def wait_for_submenu(self):
        self.wait.until(EC.presence_of_element_located(self.SUBMENU_CONTAINER))
        print("Submenú desplegado (category-menu detectado).")

    def get_subcategories(self):
        links = self.driver.find_elements(*self.SUBCATEGORY_LINK)
        subcats = [
            link for link in links
            if link.is_displayed()
            and link.text.strip()
            and link.text.strip() != "Revisar todo"
            and len(link.text.strip()) > 1
        ]
        print(f"{len(subcats)} subcategorías válidas encontradas:")
        for i, sub in enumerate(subcats):
            print(f"  [{i+1}] {sub.text} → {sub.get_attribute('data-dca-name')}")
        return subcats

    def select_random_subcategory(self, subcategories):
        sub = random.choice(subcategories)
        name = sub.text.strip()
        print(f"Seleccionando subcategoría: '{name}'")
        self.scroll_to_element(sub)
        self.click_with_human_behavior(sub)
        print(f"Click en '{name}' realizado.")
        return name

    def verify_navigation(self, expected_text):
        if not self.wait_for_url_contains("/browse/"):
            return False

        url = self.driver.current_url.lower()
        normalized = (
            expected_text.lower()
            .replace(" ", "-")
            .replace("á", "a").replace("é", "e").replace("í", "i")
            .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        )
        return normalized in url