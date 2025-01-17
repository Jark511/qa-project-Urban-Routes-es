import UrbanRoutespage
import helpers
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import ChromeOptions

        options = ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        self.driver.close()

    def test_select_comfort_fee(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        assert routes_page.get_active_comfort_state()
        #Correccion donde está el botón Comfort y  el texto del elemento con la clase tcard-title sea igual“Comfort”
        comfort_category = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.tcard.active .tcard-title'))
        )
        assert comfort_category.text== "Comfort"

        self.driver.close()

    def test_add_phone_number(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        routes_page.add_phone_number(phone_number)

        #Checar numero telefono
        assert routes_page.get_phone_number() == phone_number
        self.driver.close()

    def test_add_payment_card(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        card_number = data.card_number
        card_code = data.card_code

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        routes_page.set_payment(card_number, card_code)

        assert routes_page.get_card_check()
        self.driver.close()

    def test_set_message_for_driver(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        message = data.message_for_driver

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        routes_page.set_message(message)
        routes_page.deselect_message_box()

        assert routes_page.get_message() == message
        self.driver.close()

    def test_manta_switch(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        routes_page.click_manta_switch()

        assert routes_page.get_slider_selected()
        self.driver.close()

    def test_add_2_icecream(self):
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        routes_page.set_route(address_from, address_to)

        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        routes_page.wait_for_load_ice_plus_button()
        routes_page.scroll_to_ice_button()
        routes_page.order_n_icecream(2)

        assert routes_page.get_icecream_counter_value() == '2'
        self.driver.close()

    def test_order_taxi(self):
        # set driver
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)

        # get data
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        message = data.message_for_driver

        # set route
        routes_page.set_route(address_from, address_to)

        # select fee
        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        # add phone number
        routes_page.add_phone_number(phone_number)

        # set payment
        routes_page.set_payment(card_number, card_code)
        routes_page.click_x_close_payment_button()

        # message to driver
        routes_page.set_message(message)

        # manta y pañuelos
        routes_page.click_manta_switch()

        # order icecream
        routes_page.wait_for_load_ice_plus_button()
        routes_page.scroll_to_ice_button()
        routes_page.order_n_icecream(2)

        # order taxi
        routes_page.click_order_taxi_button()
        routes_page.wait_for_load_order_popup()

        # check pop up correct text
        assert routes_page.get_order_text() == 'Buscar automóvil'
        self.driver.close()

    def test_taxi_driver_info(self):
        # set driver
        self.setup_class()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutespage.UrbanRoutesPage(self.driver)

        # get data
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        message = data.message_for_driver

        # set route
        routes_page.set_route(address_from, address_to)

        # select fee
        routes_page.wait_for_load_fee()
        routes_page.click_comfort_fee()

        # add phone number
        routes_page.add_phone_number(phone_number)

        # set payment
        routes_page.set_payment(card_number, card_code)
        routes_page.click_x_close_payment_button()

        # message to driver
        routes_page.set_message(message)

        # manta y panuelos
        routes_page.click_manta_switch()

        # order icecream
        routes_page.wait_for_load_ice_plus_button()
        routes_page.scroll_to_ice_button()
        routes_page.order_n_icecream(2)

        # order taxi
        routes_page.click_order_taxi_button()
        routes_page.wait_for_load_order_popup()

        # wait for driver designation
        routes_page.wait_for_load_order_info_popup()

        assert 'driver.name' in routes_page.get_driver_from_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()