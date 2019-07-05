from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
start_page_url='https://www.1800contacts.com/lenses/view-all'
Expected_DOM_elem='ProductLink'
def prompt_user():
    xpaths=[]
    user_continues=True
    while user_continues:
        xpath = raw_input("Please provide an xpath you want to scrape information from: ")
        print("\n")
        elemortext= raw_input("Please provide the element name you want the text from or type \"text\" for the elements inner text: ")
        xpaths.append({xpath, elemortext})
        print("\n")
        another=raw_input("Would you like to add another xpath(Y,n)?")
        if str(another)[0].capitalize()!="Y":
            user_continues=False;
    return xpaths;
xpaths=prompt_user()
print("xpaths list:" + xpaths)
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
  
for product_url in product_urls:
    url=driver.get(product_url)
    for xpath in xpaths:
        expected_xpath=xpath[0]
        expected_element=xpath[1]
        #TODO: IF ELEMENT IS HTML ELEMENT THEN TRY BY CLASS_NAME, IF ELEMENT IS TEXT THEN SIMPLY RETURN TEXT (WARN IF BLANK)
        try:
            WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,expected_element))
            )
        except TimeoutException:
            print("could not find element " + expected_element+"! At URL="+str(product_url)+". Continuing...")
        else:
            contact_name_elem = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/lens-product-detail-page/div/div/lens-product-detail/div/div[1]/div[1]/product-header/h1')
            contact_name=contact_name_elem.text
            contact_price_elem = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/lens-product-detail-page/div/div/lens-product-detail/div/div[1]/div[1]/div/div[1]/span[2]')
            dollars=contact_price_elem.text
            cents=contact_price_elem.get_attribute("data-cents")
            contact_price=dollars+cents
            contacts_extracted_info.append({contact_name,contact_price})
            print (contacts_extracted_info)

