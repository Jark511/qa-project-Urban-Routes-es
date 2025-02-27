from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import data
import helpers


class UrbanRoutesPage:

    # Identificadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    select_taxi_button = (By.XPATH, './/div[@class="results-text"]/button[text()="Pedir un taxi"]')
    comfort_button = (By.XPATH, ".//div[@class='tariff-cards']/div[5]")
    comfort_button_active = (By.XPATH, "//div[@class='tariff-picker shown']//div[@class='tariff-cards']//div[@class='tcard active']//div[@class='tcard-title']")
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_input = (By.ID, 'phone')
    phone_next_button = (By.XPATH, ".//form/div[@class='buttons']/button[text()='Siguiente']")
    sms_input = (By.ID, 'code')
    sms_next_button = (By.XPATH, ".//form/div[@class='buttons']/button[text()='Confirmar']")
    phone_number_get = (By.CLASS_NAME, 'np-text')
    payment_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, ".//div[@class='pp-selector']/div[3]")
    payment_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR, '#code.card-input')
    card_next_button = (By.XPATH, ".//form/div[@class='pp-buttons']/button[text()='Agregar']")
    close_payment_popup = (By.XPATH, ".//div[text()='Método de pago']/../button")
    added_card_checkbox = (By.XPATH, ".//input[@id='card-1']/../span")
    message_box = (By.ID, 'comment')
    manta_switch = (By.XPATH, ".//div[text()='Manta y pañuelos']/../div[@class='r-sw']/div[@class='switch']")
    manta_switch_select = (By.XPATH, "(//input[@class='switch-input'])[1]")
    ice_plus_button = (By.XPATH, ".//div[text()='Helado']/../div[2]/div/div[@class='counter-plus']")
    ice_value_counter = (By.XPATH, ".//div[text()='Helado']/../div[2]/div/div[@class='counter-value']")
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    order_info_popup = (By.CLASS_NAME, 'order-body')
    order_info_text = (By.XPATH, ".//div[@class='order-header']/div/div[@class='order-header-title']")
    order_info_number = (By.CLASS_NAME, 'order-number')
    #Correccion de selector
    order_info_driver = (By.XPATH, ".//div[@class='order-btn-group']")

    def __init__(self, driver):
        self.driver = driver

    #Metodo de ruta
    def wait_for_load_main_page(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.from_field))

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_select_taxi(self):
        self.driver.find_element(*self.select_taxi_button).click()

    def wait_for_load_transport(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.select_taxi_button))

    def set_route(self, address_from, address_to):
        self.wait_for_load_main_page()
        self.set_from(address_from)
        self.set_to(address_to)
        self.wait_for_load_transport()
        self.click_select_taxi()

    #Metodo de tarifa
    def wait_for_load_fee(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.comfort_button))

    def click_comfort_fee(self):
        self.driver.find_element(*self.comfort_button).click()

    def get_active_comfort_state(self):
        return self.driver.find_element(*self.comfort_button_active).is_enabled()

    # Metodo numero de telefono
    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def wait_for_load_phone_popup(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.phone_number_input))

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_number_input).send_keys(phone_number)

    def click_phone_number_next_button(self):
        self.driver.find_element(*self.phone_next_button).click()

    def wait_for_load_sms_popup(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.sms_input))

    def set_sms_code(self, sms_code):
        self.driver.find_element(*self.sms_input).send_keys(sms_code)

    def click_sms_next_button(self):
        self.driver.find_element(*self.sms_next_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_get).text

    def add_phone_number(self, phone_number):
        self.click_phone_number_button()
        self.wait_for_load_phone_popup()
        self.set_phone_number(phone_number)
        self.click_phone_number_next_button()
        self.wait_for_load_sms_popup()
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.set_sms_code(sms_code)
        self.click_sms_next_button()
        self.wait_for_load_fee()

    #Metodo de pago
    def click_payment_button(self):
        self.driver.find_element(*self.payment_button).click()

    def wait_for_load_cards_popup(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.add_card_button))

    def click_add_a_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def wait_for_load_payment_popup(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.payment_input))

    def set_card_number(self, card_number):
        self.driver.find_element(*self.payment_input).send_keys(card_number)

    def wait_for_code_box(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.card_code_input))

    def select_card_code(self):
        self.driver.find_element(*self.card_code_input).click()

    def set_card_code(self, card_code):
        self.driver.find_element(*self.card_code_input).send_keys(card_code)

    def deselect_card_code(self):
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)

    def click_payment_add_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.card_next_button)).click()

    def set_payment(self, card_number, card_code):
        self.click_payment_button()
        self.wait_for_load_cards_popup()
        self.click_add_a_card_button()
        self.wait_for_load_payment_popup()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.deselect_card_code()
        self.click_payment_add_button()

    def get_card_check(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.added_card_checkbox))
        return self.driver.find_element(*self.added_card_checkbox).is_displayed()

    def click_x_close_payment_button(self):
        self.driver.find_element(*self.close_payment_popup).click()

    #Mensaje para el conductor
    def set_message(self, comment):
        self.driver.find_element(*self.message_box).send_keys(comment)

    def deselect_message_box(self):
        self.driver.find_element(*self.message_box).send_keys(Keys.TAB)

    def get_message(self):
        return self.driver.find_element(*self.message_box).get_property('value')

    #Metodo manta y pañuelo
    def click_manta_switch(self):
        self.driver.find_element(*self.manta_switch).click()

    def get_slider_selected(self):
        return self.driver.find_element(*self.manta_switch_select).is_selected()

    #Metodo helado
    def wait_for_load_ice_plus_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.ice_plus_button))

    def scroll_to_ice_button(self):
        ActionChains(self.driver).scroll_to_element(self.driver.find_element(*self.ice_plus_button)).perform()

    def click_icecream_plus_button(self):
        self.driver.find_element(*self.ice_plus_button).click()

    def get_icecream_counter_value(self):
        return self.driver.find_element(*self.ice_value_counter).text

    def order_n_icecream(self, n):
        for x in range(n):
            self.click_icecream_plus_button()

    # Metodo taxi
    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def wait_for_load_order_popup(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.order_info_popup))

    def get_order_text(self):
        return self.driver.find_element(*self.order_info_text).text

    def wait_for_load_order_info_popup(self):
        WebDriverWait(self.driver, 43).until(expected_conditions.visibility_of_element_located(self.order_info_number))

    def get_driver_from_info(self):
        return self.driver.find_element(*self.order_info_driver).text