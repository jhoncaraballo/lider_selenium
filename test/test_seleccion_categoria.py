# test/test_seleccion_categoria.py
import pytest
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# IMPORTA FUNCIÓN GLOBAL
from conftest import human_delay

@pytest.mark.usefixtures("driver")
class TestCategoriaLider:
    def test_seleccionar_categoria_al_azar(self):
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        actions = ActionChains(driver)

        print("Navegando a https://www.lider.cl/inicio...")
        driver.get("https://www.lider.cl/inicio")

        # === ESPERA INICIAL MUY HUMANA ===
        human_delay(4, 7)

        # === DETECCIÓN DE PERIMETERX (OPCIONAL) ===
        try:
            if driver.find_elements(By.CSS_SELECTOR, ".px-captcha-container, iframe[title*='verificación']"):
                print("PERIMETERX DETECTADO! Resuelve manualmente...")
                input("Presiona ENTER cuando desaparezca...")
        except:
            pass

        # === PASO 1: BUSCAR BOTÓN CATEGORÍAS ===
        btn_categorias = None
        for selector in [
            "[link-identifier='Departments']",
            #"button[data-testid='categories-button']",
            "a[href*='/inicio']",
            #"button:contains('Categorías')",
            #".header__categories"
        ]:
            try:
                btn_categorias = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                if btn_categorias.is_displayed():
                    break
            except:
                continue

        if not btn_categorias:
            driver.save_screenshot("no_boton_categorias.png")
            pytest.fail("No se encontró el botón de Categorías")

        # === MOVIMIENTO HUMANO AL BOTÓN ===
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", btn_categorias)
        human_delay(1.2, 2.8)

        # Simula cursor humano
        actions.move_to_element_with_offset(btn_categorias, random.randint(-10, 10), random.randint(-5, 5))
        actions.pause(random.uniform(0.4, 1.1))
        actions.click().perform()

        print("Botón 'Categorías' clickeado (100% humano).")
        human_delay(1.5, 3.0)

        # === PASO 2: ESPERAR MENÚ ===
        try:
            menu = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[link-identifier="Ir a la Categoría"]'))
            )
            print("Menú desplegado.")
        except TimeoutException:
            driver.save_screenshot("menu_no_aparece.png")
            pytest.fail("Menú no se desplegó")

        # === PASO 3: OBTENER CATEGORÍAS ===
        try:
            categorias = menu.find_elements(By.CSS_SELECTOR, "a[href*='/catalogo/'], a[href*='/categoria/']")
            categorias = [
                c for c in categorias
                if c.is_displayed() and c.text.strip() and len(c.text.strip()) > 2 and "Ver todo" not in c.text
            ]
            print(f"{len(categorias)} categorías válidas encontradas.")
            if not categorias:
                pytest.fail("No hay categorías visibles")
        except Exception as e:
            driver.save_screenshot("error_categorias.png")
            pytest.fail(f"Error al leer categorías: {e}")

        # === PASO 4: SELECCIONAR AL AZAR ===
        categoria = random.choice(categorias)
        nombre = categoria.text.strip()
        print(f"Seleccionando: '{nombre}'")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", categoria)
        human_delay(0.9, 2.1)

        actions.move_to_element_with_offset(categoria, random.randint(-8, 8), random.randint(-4, 4))
        actions.pause(random.uniform(0.5, 1.2))
        actions.click().perform()

        # === PASO 5: VERIFICAR ===
        try:
            wait.until(lambda d: "/catalogo/" in d.current_url or "/categoria/" in d.current_url)
            assert nombre.lower() in driver.title.lower() or nombre.lower() in driver.current_url.lower()
            print(f"ÉXITO: '{nombre}' cargada → {driver.current_url}")
        except:
            driver.save_screenshot(f"fallo_{nombre.replace(' ', '_')}.png")
            pytest.fail(f"No se cargó la categoría: {nombre}")