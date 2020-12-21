import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class RoamingAbroadScraper:
    """
    Countries Scraping
    """
    MAIN_PAGE_URL = ('http://www.three.co.uk/Support/Roaming_and_international/'
                     'Roaming_abroad')


    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='.\chromedriver')

    def run(self):
        driver = self.driver
        driver.get(self.MAIN_PAGE_URL)

        go_roam_button = driver.find_element_by_xpath(
            '//*[@title="Go Roam destinations"]'
        )
        go_roam_button.click()
        time.sleep(1)

        all_destination = driver.find_element_by_xpath('//*[@id="countries2"]')
        all_destination.click()

        result = {}

        country_titles = ['Brazil.', 'South Africa.', 'Portugal.',
        'Chile.', 'Iceland.','China.', 'Madagascar.', ]
        link_tpl = '//*[@title="{}"]'

        links = {}
        time.sleep(2)

        for title in country_titles:
            # parse links
            country_link_xpath = link_tpl.format(title)
            country_link_el = driver.find_element_by_xpath(country_link_xpath)

            country_link = country_link_el.get_attribute('href')
            links[title] = country_link

        for title in country_titles:
            result[title] = {}

            driver.get(links[title])
            time.sleep(1)

            # parse table (if you need a new value simply add it to the list)
            values = ['Calling a UK number', 'Texts to UK',
            'Receiving calls from any number','Using internet and data']

            column1_tpl = ('//th[contains(text(), "{value}")]/'
                           'following-sibling::td[1]')
            column2_tpl = ('//th[contains(text(), "{value}")]/'
                          'following-sibling::td[2]')

            for value in values:
                column1 = driver.find_element_by_xpath(
                    column1_tpl.format(value=value)
                ).text

                """
                 There are different tables so we use try.
                 As there are two types of tables - with one and two columns.
                """
                try:
                    column2 = driver.find_element_by_xpath(
                        column2_tpl.format(value=value)
                    ).text
                except NoSuchElementException:
                    # we have table with 1 column
                    result[title][value] = {
                        'Cost': column1
                    }
                else:
                    result[title][value] = {
                        'With allowance remaining': column1,
                        'Outside your allowance': column2
                    }

        print(result)

        """
        TODO: As your brief doesn't specify how the data needs to be presented,
        I decided to do it using print().
        If needed it can also be saved as a file.

        """

    def close_browser(self):
        self.driver.close()

if __name__ == '__main__':
    scraper = RoamingAbroadScraper()
    scraper.run()
    scraper.close_browser()
