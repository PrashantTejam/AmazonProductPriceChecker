from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

# Amazon Config for URL, Product and Login Credentials
import Config


class AmazonPriceCheck:
    def __init__(self, search_term, base_url):
        options = webdriver.ChromeOptions()
        # If you want to see Chrome in action "--start-maximized". This is good for few initial runs
        options.add_argument("--start-maximized")

        # open Chrome with headless mode
        # options.add_argument("--headless")

        # create driver object using driver path
        driver = webdriver.Chrome(r"C:\Users\prash\.wdm\drivers\chromedriver\win32\85.0.4183.87\chromedriver.exe",
                                  options=options)
        action = ActionChains(driver)

        # assigning website
        driver.get('http://www.amazon.co.uk')
        driver.implicitly_wait(2)

        # Signing into Amazon is not required to get the product information
        # this is the part where I need to imagine Amazon website browsing action. 'Inspect' is your friend here.
        first_level_menu = driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/span[1]')
        action.move_to_element(first_level_menu).perform()
        driver.implicitly_wait(2)

        # Login to Amazon
        second_level_menu = driver.find_element_by_xpath('//*[@id="nav-flyout-ya-signin"]/a/span')
        second_level_menu.click()
        driver.implicitly_wait(2)

        # For Login - Email
        signinelement = driver.find_element_by_xpath('//*[@id="ap_email"]')
        signinelement.send_keys(Config.USERNAME)
        driver.implicitly_wait(1)

        cont = driver.find_element_by_xpath('//*[@id="continue"]')
        cont.click()
        driver.implicitly_wait(1)

        # For Login - Password
        passwordelement = driver.find_element_by_xpath('//*[@id="ap_password"]')
        passwordelement.send_keys(Config.PASSWORD)
        driver.implicitly_wait(1)

        # click search button
        login = driver.find_element_by_xpath('//*[@id="signInSubmit"]')
        login.click()
        driver.implicitly_wait(5)

        # create WebElement for a search box
        sign_in_element_box = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        sign_in_element_box.send_keys(Config.SEARCHKEYWORD)

        search_button = driver.find_element(By.ID, 'nav-search-submit-button')
        search_button.click()

        driver.implicitly_wait(10)

        product_asin = []
        product_name = []
        product_price = []
        product_link = []

        items_list = Wait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
        for item in items_list:
            # find product name
            name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
            product_name.append(name.text)

            # find the ASIN number
            data_asin = item.get_attribute("data-asin")
            product_asin.append(data_asin)

            # find product price
            whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
            fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

            if whole_price != [] and fraction_price != []:
                price = '.'.join([whole_price[0].text, fraction_price[0].text])
            else:
                price = 0
            product_price.append(price)

            # find product link. This is tricky. Amazon changed class 3 times in last 10 months :(
            link = item.find_element(By.XPATH,
                                     './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute(
                "href")
            product_link.append(link)

        # TODO - Add logic to compare price, add to cart and send email

        driver.quit()

        # to check data scraped
        print(product_name)
        print(product_asin)
        print(product_price)
        print(product_link)


if __name__ == '__main__':
    am = AmazonPriceCheck(Config.SEARCHKEYWORD, Config.BASE_URL)
