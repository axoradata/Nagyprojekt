from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select

def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

# Böngésző indítása
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    driver.get("http://localhost:5173/login")
    driver.maximize_window()

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_email"))
    )
    slow_type(email_input, "admin") 

    pass_input = driver.find_element(By.ID, "login_password")
    slow_type(pass_input, "1234")

    login_btn = driver.find_element(By.ID, "login_button")
    time.sleep(1)
    login_btn.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )
    
    print("Sikeres E2E teszt: A bejelentkezés és az átirányítás lefutott!")
    
    token = driver.execute_script("return localStorage.getItem('token');")
    if token:
        print(f"Token sikeresen elmentve: {token[:10]}...")

    time.sleep(1)

    login_btn = driver.find_element(By.ID, "nav-profile")
    time.sleep(3)
    login_btn.click()

    driver.execute_script("window.scrollTo({top: 500, behavior: 'smooth'});")
    time.sleep(1)

    theme_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "theme_selector"))
    )

    select = Select(theme_dropdown)
    select.select_by_value("light")
    time.sleep(3)

    login_btn = driver.find_element(By.ID, "nav-users")
    time.sleep(3)
    login_btn.click()

    login_btn = driver.find_element(By.ID, "nav-groups")
    time.sleep(3)
    login_btn.click()

    login_btn = driver.find_element(By.ID, "nav-logs")
    time.sleep(3)
    login_btn.click()

    login_btn = driver.find_element(By.ID, "nav-rfid")
    time.sleep(3)
    login_btn.click()

    login_btn = driver.find_element(By.ID, "nav-logout")
    time.sleep(3)
    login_btn.click()

except Exception as e:
    print(f"Hiba történt a teszt során: {e}")
    try:
        error_text = driver.find_element(By.ID, "error_display").text
        print(f"Frontend hibaüzenete: {error_text}")
    except:
        pass

finally:
    driver.quit()