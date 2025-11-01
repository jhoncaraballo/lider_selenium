import pytest
from pages.home_page import HomePage
from pages.category_menu_page import CategoryMenuPage

@pytest.mark.usefixtures("driver")
class TestCategoriaLider:

    def test_seleccionar_categoria_al_azar(self, driver):
        home = HomePage(driver)
        menu = CategoryMenuPage(driver)

        # 1. Navegar
        home.navigate()
        home.handle_perimeterx()

        # 2. Abrir menú
        home.open_categories_menu()

        # 3. Obtener categorías
        menu.wait_for_menu()
        categories = menu.get_main_categories()
        assert categories, "No se encontraron categorías"

        # 4. Seleccionar categoría principal
        cat_name = menu.select_random_main_category(categories)

        # 5. Submenú
        menu.wait_for_submenu()
        subcategories = menu.get_subcategories()
        assert subcategories, "No se encontraron subcategorías"

        # 6. Seleccionar subcategoría
        sub_name = menu.select_random_subcategory(subcategories)

        # 7. Verificar
        assert menu.verify_navigation(sub_name), f"No se encontró '{sub_name}' en la URL"
        print(f"ÉXITO: '{sub_name}' cargada → {driver.current_url}")