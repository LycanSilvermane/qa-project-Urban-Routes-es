import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # Definir las tuples para localizar elementos
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi = (By.XPATH, '//button[text() = "Pedir un taxi"]')
    comfort_price = (By.XPATH, '//div[text() = "Comfort"]')
    phone_button = (By.CLASS_NAME, "np-button")
    phone_field = (By.ID, "phone")
    phone_code = (By.XPATH, '//input[@placeholder="xxxx"]')
    confirm_phone_code = (By.XPATH, '//button[text() = "Confirmar"]')
    next_button = (By.CLASS_NAME, "full")
    payment_method_button = (By.XPATH, '//div[@class="pp-button filled" and .//div[text()="Método de pago"]]')
    add_card = (By.XPATH, '//div[text() = "Agregar tarjeta"]')
    card_number_field = (By.ID, 'number')
    code_field = (By.XPATH, '//input[@placeholder="12"]')
    another_click = (By.CLASS_NAME, "plc")
    add_button = (By.XPATH, '//button[text() = "Agregar"]')
    close_payment_method_overlay = (By.XPATH, '//div[contains(@class, "head") and normalize-space()="Método de pago"]/../button[@class="close-button section-close"]')
    driver_message = (By.ID, 'comment')
    switch_for_blanket = (By.XPATH, '//div[contains(@class,"r-sw-label") and normalize-space()="Manta y pañuelos"]/../div[@class="r-sw"]/div[@class="switch"]/span[@class="slider round"]') #input[@type="checkbox"]
    add_icecream = (By.XPATH, '//div[contains(@class, "r-counter-label") and normalize-space()="Helado"]/../div[@class="r-counter"]/div[@class="counter"]/div[@class="counter-plus"]')
    search_taxi = (By.CLASS_NAME, "smart-button")


    def __init__(self, driver):
        self.driver = driver

# Definir una espera hasta que la página cargue por completo

    def wait_for_load_home_page(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.from_field))

# b xc Definir una espera explicita hasta que el boton para solicitar taxi esté disponible

    def wait_for_call_taxi_button(self):
        WebDriverWait(self.driver,10).until(expected_conditions.visibility_of_element_located(self.call_taxi))

# Definir espera hasta que el form de tarjeta aparezca

    def wait_for_card_form(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.add_card))

# Definir espera hasta que la selección de método de pago esté disponible

    def wait_for_select_payment_method(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.payment_method_button))

# Definir espera para el campo card number

    def wait_for_card_number_field(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.card_number_field))

# Definir espera para cerrar overlay de método de pago

    def wait_close_payment_method_overlay_button(self):
        return WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.close_payment_method_overlay))

# Espera para hacer clic en manta y pañuelos
    def wait_for_blanket_button(self):
        return WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.switch_for_blanket))

# Esperar el boton + del helado
    def wait_plus_button_icecream(self):
        return WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.add_icecream))

# Definir el método para rellenar la información del formulario Desde

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

# Hacer lo mismo de antes con el formulario Hasta

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

# Obtener el valor que se encuentra en el campo Desde

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

# Obtener el valor que se encuentra en el campo Hasta

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

# Obtener valor del campo comfort

    def get_comfort_price(self):
        return self.driver.find_element(*self.comfort_price).text

# Obtener phone number

    def get_phone_number(self):
        return self.driver.find_element(By.CLASS_NAME, "np-text").text

# Obtener card number

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_attribute('value')

# Obtener el mensaje al conductor

    def get_message_for_driver(self):
        return self.driver.find_element(*self.driver_message).get_attribute('value')


# Método que rellena los campos desde y hasta, espera que aparezca el botón y hace clic en él

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.wait_for_call_taxi_button()
        self.driver.find_element(*self.call_taxi).click()

# Método que hace clic en la opción comfort

    def set_comfort_price(self):
        self.driver.find_element(*self.comfort_price).click()

# Método que rellena la sección de número telefónico

    def set_phone_number(self):
        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_field).send_keys(data.phone_number)
        self.driver.find_element(*self.next_button).click()

# Método que rellena el campo código SMS

    def set_phone_code(self,phone_code):
        self.driver.find_element(*self.phone_code).send_keys(phone_code)
        self.driver.find_element(*self.confirm_phone_code).click()

# Método para rellenar el campo tarjeta

    def set_card_number(self):
        self.driver.find_element(*self.payment_method_button).click()
        UrbanRoutesPage.wait_for_card_form(self)
        self.driver.find_element(*self.add_card).click()
        UrbanRoutesPage.wait_for_card_number_field(self)
        self.driver.find_element(*self.card_number_field).send_keys(data.card_number)
        self.driver.find_element(*self.code_field).send_keys(data.card_code)

    def set_save_card_details(self):
        self.driver.find_element(*self.another_click).click()
        self.driver.find_element(*self.add_button).click()
        close_button = UrbanRoutesPage.wait_close_payment_method_overlay_button(self)
        self.driver.execute_script("arguments[0].click();", close_button)

# Rellena el campo mensaje para el conductor

    def set_driver_message(self):
        self.driver.find_element(*self.driver_message).send_keys(data.message_for_driver)

# Activa la opción cobija y pañuelos

    def set_blanket(self):
        switch_for_blanket = UrbanRoutesPage.wait_for_blanket_button(self)
        self.driver.execute_script("arguments[0].click();", switch_for_blanket)

# Añade 2 helados

    def set_icecream(self):
        more_icecream = self.driver.find_element(*self.add_icecream)
        for i in range(2):
            more_icecream.click()

# Busca el taxi disponible para el viaje

    def set_search_taxi(self):
        self.driver.find_element(*self.search_taxi).click()

# Clase para el modal del conductor

class OrderOverlay:
    order_overlay_timer = (By.XPATH, '//div[contains(@class, "order-header-time")]')
    taxi_driver_name  = (By.XPATH, '//div[@class="order-number"]')

    def __init__(self, driver):
        self.driver = driver

# Espera para la aparición del Modal

    def wait_for_order_overlay(self):
        WebDriverWait(self.driver, 200).until(expected_conditions.visibility_of_element_located(self.order_overlay_timer))

# Espera hasta que la información del conductor aparezca

    def wait_driver_name(self):
        WebDriverWait(self.driver, 200).until(expected_conditions.visibility_of_element_located(self.taxi_driver_name))

# Obtener nombre del conductor

    def get_taxi_driver_name(self):
        return self.driver.find_element(*self.taxi_driver_name).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        """"from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)"""""
        #el anterior codigo solo funciona con versiones de selenium anteriores a versiones 4.xx
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_comfort_price(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        assert routes_page.get_comfort_price() == "Comfort"

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        assert routes_page.get_phone_number() == data.phone_number

    def test_set_card_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        assert routes_page.get_card_number() == data.card_number

    def test_set_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        routes_page.set_save_card_details()
        routes_page.set_driver_message()
        assert routes_page.get_message_for_driver() == data.message_for_driver

    def test_set_blanket(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        routes_page.set_save_card_details()
        routes_page.set_driver_message()
        routes_page.set_blanket()
        switch = self.driver.find_element(By.CSS_SELECTOR, ".switch-input")
        assert switch.is_selected(), "El switch no quedó activo"

    def test_set_icecream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        routes_page.set_save_card_details()
        routes_page.set_driver_message()
        routes_page.set_blanket()
        routes_page.wait_plus_button_icecream()
        routes_page.set_icecream()
        icecream_count = self.driver.find_element(By.XPATH, '//div[contains(@class, "r-counter-label") and normalize-space()="Helado"]/../div[@class="r-counter"]/div[@class="counter"]/div[@class="counter-value"]').text
        assert icecream_count == "2"

    def test_set_search_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        routes_page.set_save_card_details()
        routes_page.set_driver_message()
        routes_page.set_blanket()
        routes_page.set_search_taxi()
        modal_page = OrderOverlay(self.driver)
        modal_page.wait_for_order_overlay()
        taxi_overlay = self.driver.find_element(*OrderOverlay.order_overlay_timer)
        assert taxi_overlay.is_displayed(), "El overlay no esta activo"

    def test_driver_name(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort_price()
        routes_page.set_phone_number()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.wait_for_select_payment_method()
        routes_page.set_card_number()
        routes_page.set_save_card_details()
        routes_page.set_driver_message()
        routes_page.set_blanket()
        routes_page.set_search_taxi()
        modal_page = OrderOverlay(self.driver)
        modal_page.wait_for_order_overlay()
        modal_page.wait_driver_name()
        name_of_taxi_driver = self.driver.find_element(*OrderOverlay.taxi_driver_name).text
        assert modal_page.get_taxi_driver_name() == name_of_taxi_driver


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
