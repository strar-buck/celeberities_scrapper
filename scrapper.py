from selenium import webdriver  # Need To import webdriver from selenium package
from urllib.request import urlretrieve
import requests
from string import ascii_lowercase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException , StaleElementReferenceException

from time import sleep  

url_list = [
     "https://en.wikipedia.org/wiki/Category:Indian_male_film_actors",
     "https://en.wikipedia.org/wiki/Category:Indian_film_actresses",
     "https://en.wikipedia.org/wiki/Category:Indian_male_television_actors",
     "https://en.wikipedia.org/wiki/Category:Indian_television_actresses"
    # "https://en.wikipedia.org/wiki/Category:American_male_film_actors",
    # "https://en.wikipedia.org/wiki/Category:American_film_actresses",
    # "https://en.wikipedia.org/wiki/Category:American_male_television_actors",
    # "https://en.wikipedia.org/wiki/Category:American_television_actresses"
] 
wikki_url = "https://en.wikipedia.org/wiki/{0}"

browser = webdriver.Chrome(executable_path='/Users/ritu/Downloads/chromedriver')
celeberities = []

indian_celeberity = open("data/celeberity/indian.txt","w")
# us_celeberity = open("data/celeberity/US.txt","w")


for url in url_list:
    is_next_link = True
    browser.get(url) 
    while is_next_link:
        default_handle =  browser.current_window_handle
        headings = browser.find_elements_by_xpath('//*[@id="mw-pages"]/div/div/div')
        for heading_instance in headings:
            sel_instance_list = heading_instance.find_elements_by_xpath('ul/li')
            for instance in sel_instance_list:
                indian_celeberity.write(str(instance.text) + "\n")
                celeberities.append(instance.text)
        next_link = browser.find_element_by_xpath('//*[@id="mw-pages"]/a[1]')
        if next_link.text == "previous page":
            next_link = browser.find_element_by_xpath('//*[@id="mw-pages"]/a[2]')
        tmp_text = next_link.text
        if tmp_text == "next page":
            next_link.click()
        else:
            is_next_link = False


# celeberities = open("data/celeberity/indian.txt").readlines()

for name in celeberities[1:]:
    browser.get(wikki_url.format(name))
    name = "_".join(name.split())
    try:
        try:
            img_instance = browser.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[2]/td/a/img[@src]')
        except:
            img_instance = browser.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/a/img[@src]')
        image_url = img_instance.get_attribute('src')
        # Download Imgae  
        with open('images/indian_celeberity/' + name + '.jpg', 'wb') as f:
            f.write(requests.get(image_url).content)
        # browser.switch_to.window(default_handle)
    except:
        browser.get("http://google.com") 
        inputElement = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')
        inputElement.send_keys(name)
        inputElement.submit()
        tab_list = browser.find_elements_by_xpath('//*[@id="hdtb-msb-vis"]/div/a')
        for tab in tab_list:
            if tab.text == "Images":
                tab.click() 
                image_instance = browser.find_element_by_xpath('//*[@id="rg_s"]/div[1]/a[1]/img[@src]')
                image_url = image_instance.get_attribute('src')
                urlretrieve(image_url, "images/indian_celeberity/" +  name + ".jpg")
                break

browser.close()
