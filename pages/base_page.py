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