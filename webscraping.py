import atexit
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
start_page_url='https://www.1800contacts.com/lenses'
Expected_DOM_elem='ProductLink'
def prompt_user():
    xpaths=[]
    another_xpath=True
    while another_xpath:
        xpath_text = raw_input("Please provide an xpath you want to scrape information from in the form(relative: //tagname[@attribute=value] or absolute: '/html/.../' ): ")
        dict_of_xpath_elems={}
        list_of_elems=[]
        another_elem=True
        while another_elem:
            elemortext= raw_input("Please provide the element name you want the text from or type \"text\" for the elements inner text: ")
            list_of_elems.append(elemortext)
            while True:
                another=raw_input("Would you like to add another element(Y,n)?")
                try:
                    if str(another)[0].lower()=='n':
                        print('if')
                        another_elem=False
                        break
                    elif str(another)[0].capitalize()=='Y':
                        print('elif')
                        break
                    else:
                        print('else')
                        continue
                except(IndexError):
                    continue
        dict_of_xpath_elems[xpath_text]=list_of_elems
        xpaths.append(dict_of_xpath_elems)
        while True:
            another=raw_input("Would you like to add another xpath(Y,n)?")
            try:
                if str(another)[0].lower()=='n':
                    print('if')
                    another_xpath=False
                    break
                elif str(another)[0].capitalize()=='Y':
                    print('elif')
                    break
                else:
                    print('else')
                    continue
            except(IndexError):
                continue
    return xpaths;

xpaths=prompt_user()
print(xpaths)

driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities={'browserName':'chrome', 'platform':'WINDOWS'})
try:
    url=driver.get(start_page_url)
    element=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME,Expected_DOM_elem))
    )
except TimeoutException:
    raise TimeoutException('The URL:"'+start_page_url+'" does not have the DOMElement:"'+Expected_DOM_elem+'"')	
products=driver.find_elements_by_class_name('ProductLink')
product_urls=[]
contacts_extracted_info = []
for product in products:
    product_urls.append(product.get_attribute('href'))
first=True;
#TODO: dict_of_results structured like so {"url": "", "xpath": "", "info":""} I'm going to want to be able to get multiple attributes per xpath pass instead of repeating the same xpath for a different element
list_of_results=[] 
for product_url in product_urls:
    dict_of_url_info={}
    dict_of_url_info['url']=product_url
    list_of_results.append(dict_of_url_info)	
    url=driver.get(product_url)
    for dict_of_xpath_and_elems in xpaths:
        for xpath, elems in dict_of_xpath_and_elems.items():
          expected_xpath=xpath.lower()
          try:
              WebDriverWait(driver,10).until(
              EC.presence_of_element_located((By.XPATH,expected_xpath))
              )
          except TimeoutException:
              print("could not find xpath " + expected_xpath+"! At URL="+str(product_url)+". Continuing...")
          else:
            dict_of_url_info["xpath"]=expected_xpath
            dom_xpath_obj = driver.find_element_by_xpath(expected_xpath)
            for expected_element in elems:
                if expected_element=="text":
                    info=dom_xpath_obj.text
                    dict_of_url_info["info"]=info
                else:
                    info=dom_xpath_obj.get_attribute(expected_element)
                    dict_of_url_info["info"]=info
    print(list_of_results)

