from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
import data
import helpers
import time

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

        # Verificar se a URL não expirou
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 2).until(lambda d: True)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert routes_page.get_from_location_value() == data.ADDRESS_FROM
        assert routes_page.get_to_location_value() == data.ADDRESS_TO
        time.sleep(3)

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_taxi_option()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert routes_page.click_comfort_active()
        time.sleep(3)

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_number_text(data.PHONE_NUMBER)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert data.PHONE_NUMBER in routes_page.numero_confirmado()
        time.sleep(3)

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert "Cartão" in routes_page.confirm_cartao()
        time.sleep(3)

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        message = data.MESSAGE_FOR_DRIVER
        routes_page.set_message_for_driver(message)
        assert routes_page.get_message_for_driver() == message
        time.sleep(3)

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.switch_cobertor()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert routes_page.switch_cobertor_active() is True
        time.sleep(3)

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        for _ in range(2):
            routes_page.add_ice()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert int(routes_page.qnt_sorvete()) == 2
        time.sleep(3)

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_number_text(data.PHONE_NUMBER)
        WebDriverWait(self.driver, 1).until(lambda d: True)
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        WebDriverWait(self.driver, 2).until(lambda d: True)
        routes_page.call_taxi()
        WebDriverWait(self.driver, 1).until(lambda d: True)
        assert "Buscar carro" in routes_page.pop_up_show()
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()