'''Запускать через $ pytest -s -p no:pycashe simbir.py --alluredir=allure-results
    Команда для вывода отчета $ '''
import pytest
import allure,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

print("Импорт модулей выполнен успешно!")

# Определение функции driver
@pytest.fixture
def driver():
    print("Инициализация драйвера...")
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.83 Safari/537.36")
    options.add_argument("accept-language=ru,en-US;q=0.9,en;q=0.8")
    options.add_argument("accept-encoding=gzip, deflate, br, zstd")
    options.add_argument("content-type=application/json")
    options.add_argument("sec-ch-ua-platform=\"Linux\"")
    chromedriver_path = "/usr/local/bin/chromedriver" # Путь к chromedriver

    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        print("Драйвер инициализирован успешно!")
        driver.maximize_window()
        yield driver
    except Exception as e:
        print(f"Ошибка инициализации драйвера: {e}")
    finally:
        driver.quit()
        print("Драйвер остановлен.")

print("Функция driver определена успешно!")

# Определение класса FormPage (страница формы)
class FormPage:
    URL = "https://practice-automation.com/form-fields/"

    def __init__(self, driver):
        self.driver = driver
        print("Инициализация страницы формы...")

    def load(self):
        self.driver.get(self.URL)
        print("Страница формы загружена успешно!")

    def fill_name(self, name):
        self.driver.find_element(By.ID, "name-input").send_keys(name)

    def fill_password(self, password):
        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)

    def select_favorite_drinks(self):
        self.driver.find_element(By.XPATH, "//input[@value='Milk']").click()
        self.driver.find_element(By.XPATH, "//input[@value='Coffee']").click()

    def select_favorite_color(self, color="Yellow"):
        color_element = self.driver.find_element(By.XPATH, f"//input[@name='fav_color' and @value='{color}']")
        self.driver.execute_script("arguments[0].click();", color_element)

    def select_like_automation(self):
        select_element = self.driver.find_element(By.ID, "automation")
        select = Select(select_element)
        select.select_by_value("yes")

    def fill_email(self, email):
        self.driver.find_element(By.ID, "email").send_keys(email)

    def get_automation_tools(self):
        label_element = self.driver.find_element(By.XPATH, "//label[text()='Automation tools']")
        ul_element = label_element.find_element(By.XPATH, "following-sibling::ul")
        tools_elements = ul_element.find_elements(By.TAG_NAME, "li")
        toolnames = [tool.text for tool in tools_elements]
        lentools = len(toolnames)
        maxtool = max(toolnames, key=len)
        return lentools, maxtool

    def fill_message(self, message):
        self.driver.find_element(By.ID, "message").send_keys(message)

    def submit_form(self):
        element = self.driver.find_element(By.ID, "submit-btn")
        self.driver.execute_script("arguments[0].click();", element)

    def get_alert_text_and_accept(self):
        alert = Alert(self.driver)
        alert_text = alert.text
        alert.accept()
        return alert_text

# Определение теста с использованием Allure
@allure.feature('Form Submission Test')
@allure.story('Test the form submission and validation')
@allure.severity(allure.severity_level.NORMAL)
def test_form_submission(driver):
    page = FormPage(driver)
    page.load()

    allure.step("Заполняем поле имени")
    page.fill_name("Makeximu")
    allure.attach('Шаг 1: Заполняем поле имени', 'Заполняем поле имени. Ввелось успешно.', allure.attachment_type.TEXT)

    allure.step("Заполняем поле пароля")
    page.fill_password("TestPassword123")
    allure.attach('Шаг 2: Заполняем поле пароля', 'Заполняем поле пароля. Ввелось успешно.', allure.attachment_type.TEXT)

    allure.step("Выбираем любимые напитки")
    page.select_favorite_drinks()
    allure.attach('Шаг 3: Выбираем любимые напитки', 'Выбираем любимые напитки. Выбрано успешно.', allure.attachment_type.TEXT)

    allure.step("Выбираем любимый цвет")
    page.select_favorite_color()
    allure.attach('Шаг 4: Выбираем любимый цвет', 'Выбираем любимый цвет. Выбрано успешно.', allure.attachment_type.TEXT)

    allure.step("Выбираем автоматизацию")
    page.select_like_automation()
    allure.attach('Шаг 5: Выбираем автоматизацию', 'Выбираем автоматизацию. Выбрано успешно.', allure.attachment_type.TEXT)

    allure.step("Заполняем электронную почту")
    page.fill_email("mytonovmax1105@gmail.com")
    allure.attach('Шаг 6: Заполняем электронную почту', 'Заполняем электронную почту. Ввелось успешно.', allure.attachment_type.TEXT)

    allure.step("Получаем информацию о инструментах автоматизации")
    lentools, maxtool = page.get_automation_tools()
    allure.attach('Шаг 7: Получаем информацию о инструментах автоматизации', 'Получаем информацию о инструментах автоматизации. Получено успешно.', allure.attachment_type.TEXT)

    allure.step(f"Заполняем сообщение: Количество инструментов: {lentools}, Максимальный: {maxtool}")
    page.fill_message(f"Количество инструментов: {lentools} Максимальный: {maxtool}")
    allure.attach('Шаг 8: Заполняем сообщение', 'Заполняем сообщение. Ввелось успешно.', allure.attachment_type.TEXT)

    allure.step("Отправляем форму")
    page.submit_form()
    allure.attach('Шаг 9: Отправляем форму', 'Отправляем форму. Отправлено успешно.', allure.attachment_type.TEXT)

    allure.step("Проверяем сообщение от alert")
    alert_text = page.get_alert_text_and_accept()
    allure.attach('Шаг 10: Проверяем сообщение от alert', 'Проверяем сообщение от alert. Проверено успешно.', allure.attachment_type.TEXT)
    
    assert alert_text == "Message received!"
    print("Форма успешно отправлена!")