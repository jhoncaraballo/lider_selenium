import pytest
import undetected_chromedriver as uc
import random
import time
import json
from selenium import webdriver

# === FUNCIÓN GLOBAL DE DELAY HUMANO ===
def human_delay(min_s=0.8, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

# === DRIVER CON MÁXIMA STEALTH ===
@pytest.fixture(scope="class")
def driver(request):
    print("Iniciando Chrome 141 (MÁXIMA STEALTH vs PerimeterX)...")

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only=false")
    options.add_argument("--no-first-run")
    options.add_argument("--safebrowsing-disable-auto-update")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")

    # USER AGENT REAL
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.123 Safari/537.36"
    )

    # === INICIA DRIVER ===
    driver = uc.Chrome(options=options, version_main=141, headless=False)

    # === STEALTH SCRIPT (EJECUTAR ANTES DE CARGAR CUALQUIER PÁGINA) ===
    stealth_script = """
    Object.defineProperty(navigator, 'webdriver', {get: () => false});
    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['es-CL', 'es']});
    Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
    Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
    Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'});
    window.chrome = { runtime: {}, app: {}, csi: function(){}, loadTimes: function(){} };
    Object.defineProperty(screen, 'colorDepth', {get: () => 24});
    Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
    delete navigator.__proto__.webdriver;
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_script})

    driver.implicitly_wait(10)

    # === PASA FUNCIÓN AL TEST ===
    request.cls.driver = driver
    request.cls.human_delay = human_delay

    yield driver
    print("Cerrando navegador...")
    driver.quit()