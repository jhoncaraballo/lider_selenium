import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from pages.home_page import HomePage

@pytest.mark.usefixtures("driver")
class TestCarroCompras:

    def test_click_banner_y_primer_producto(self):
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        home = HomePage(driver)

        # 1. Navegar con HomePage 
        home.navigate()
        assert "/inicio" in driver.current_url
        print("Home cargada.")

        # 2. Click en banner 
        home.click_first_banner()

        # 3. Esperar lista de productos

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dca-name='ui_product_tile:vertical_index'] > a"))
        )
        home.human_delay(1, 2)
        print("Lista de productos visible.")

        # 4. Click en primer producto

        first_product = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,"div[data-dca-name='ui_product_tile:vertical_index'] > a")
            )
        )
        product_text = first_product.text.strip() or "Producto sin nombre"
        home.scroll_to_element(first_product)
        home.click_with_human_behavior(first_product)       
        print(f"Clic en primer producto: '{product_text}'")

        # 5. Click en agregar al carro

        add_product = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,"button[aria-label*='Agregar al carro']")
            )
        )
        home.click_with_human_behavior(add_product)

        # 6. Click en carro de compras

        button_car = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,"#cart-button-header")
            )
        )
        home.click_with_human_behavior(button_car)

        # 7. Verificar URL del carro de compras

        assert "/cart" in driver.current_url
        print("Carro de compras cargo.")

        # 8. Verificar producto en carro - USAR ESTA VERSIÓN
        count_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.f2.mid-gray.ml1"))
        )

        # 9. Extraer el texto y parsear el número
        count_text = count_element.text
        print(f"Texto del contador: '{count_text}'")

        import re
        match = re.search(r'\((\d+) productos?\)', count_text)
        if match:
            product_count = int(match.group(1))

            # Validar el contador
            if product_count == 0:
                raise AssertionError(f"ERROR: El carrito está vacío (0 productos)")
            elif product_count >= 1:
                print(f"ÉXITO: Finalizó correctamente. Productos en carrito: {product_count}")
            else:
                raise ValueError(f"ERROR: Valor inválido de productos: {product_count}")
        else:
            raise ValueError(f"ERROR: No se pudo extraer el número de productos del texto: '{count_text}'")