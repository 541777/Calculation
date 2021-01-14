from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:\\Users\\vbaskaran\\Documents\\django_p\\projects\\selenium\\chromedriver.exe")


driver.get("http://127.0.0.1:8000/maturity1/")
driver.find_element_by_id('policy').send_keys('A100003')




driver.find_element_by_id('sub').click()

