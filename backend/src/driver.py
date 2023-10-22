import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities

class Driver:

    def __init__(self):
        """
        We need to deal with the user agent.
        Restart the driver each query to avoid bots.
        :return: None
        """

        profile = webdriver.FirefoxProfile()

        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('headless', True)
        profile.set_preference("general.useragent.override",
                               f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/{random.randint(5, 500)}.{random.randint(5, 100)} (KHTML, like Gecko) Chrome/{random.randint(100, 120)}.0.{random.randint(5, 5000)}.{random.randint(100, 120)} Safari/{random.randint(100, 520)}.{random.randint(1, 120)}")
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        driver = webdriver.Firefox(
            firefox_profile=profile,
            desired_capabilities=desired
        )

        self.driver = driver

    def handle_cookie(self,element,xpath,url):
        """
        Element : The HTML element we will use to find the button.
        xpath :         button[@class=
        url : the URL we want to search
        :return:
        """
        WAIT_TIME=12
        WebDriverWait(self.driver, random.randint(5, 10))
        self.driver.get(url)
        wait = WebDriverWait(self.driver, random.randint(WAIT_TIME / 2, WAIT_TIME))
        before = f"//{xpath}'{element}']"
        wait.until(EC.element_to_be_clickable((By.XPATH, before))).click()

    def search(self, element, element_type):
            """
            Pattern match and find the elements at the top of the page that have best cheapest and fastest.
            :return:
            """

            matching_elements = self.driver.find_elements(By.XPATH,f"//*[contains({element_type}, '{element}')]")
            return matching_elements

    def finish(self):
        self.driver.quit()
