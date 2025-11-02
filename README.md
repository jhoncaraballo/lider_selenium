# lider_selenium

# Framework de automatización de pruebas para Lider.cl desarrollado en Python con Selenium y Pytest.

# Descripción
Este proyecto contiene tests automatizados para las funcionalidades  de Lider.cl, incluyendo:

- Flujo de compras (agregar productos al carrito)
- Sistema de login
- Navegación por categorías
- Interacción con banners promocionales

## Tecnologías Utilizadas
- Python 3.13+
- Selenium WebDriver
- undetected-chromedriver (para evitar detección)
- Pytest Framework de testing
- Pytest-html para reportes

## Archivo .env

- Ingresa un mail valido para la prueba

## Instalacion
1. Clonar repositorio 
        git clone <https://github.com/jhoncaraballo/lider_selenium>
        cd lider_selenium

2. Crear entorno virtual
        python -m venv venv
        source venv/bin/activate  # Linux/Mac
        venv\Scripts\activate     # Windows

3. Instalar dependencias
        pip install -r requeriments.txt

## Ejecucion de pruebas
De la siguiente manera se ejecutara el test y se generara un reporte con el resultado del test

- Ejecutar todos los test
        pytest test/ -v --html=report.html -s

- Ejecutar individualmente
        pytest test/test_seleccion_categoria.py -v --html=report_categoria.html -s
        pytest test/test_carro_compras.py -v --html=report_carro.html -s   
        pytest test/test_login.py -v --html=report_login.html -s   
