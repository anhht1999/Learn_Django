# import libary
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re #regex
# import urllib.request

# crwal data lazada
def load_url_selenium_lazada(url):
    # Selenium
    driver=webdriver.Chrome(executable_path='/usr/bin/chromedriver')
    print("Loading url=", url)
    driver.get(url)
    list_review = []
    # just craw 10 page
    x=0
    while x<10:
        try:
            #Get the review details here
            WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.item")))
        except:
            print('No has comment')
            break
        
        product_reviews = driver.find_elements_by_css_selector("[class='item']")
        # Get product review
        for product in product_reviews:
            review = product.find_element_by_css_selector("[class='content']").text
            if (review != "" or review.strip()):
                print(review, "\n")
                list_review.append(review)
        #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        if len(driver.find_elements_by_css_selector("button.next-pagination-item.next[disabled]"))>0:
            break;
        else:
            button_next=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-pagination-item.next")))
            driver.execute_script("arguments[0].click();", button_next)
            print("next page")
            time.sleep(2)
            x +=1
    driver.close()
    return list_review

# crawl data tiki
def load_url_selenium_tiki(url):
    driver=webdriver.Chrome(executable_path='/usr/bin/chromedriver')
    print("Loading url=", url)
    driver.get(url)
    list_review = []
    # just craw 10 page
    x=0
    while x<10:
        try:
          
            #Get the review details here
            WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.review-comment")))
        except :
            print('Not has comment!')
            break
        product_reviews = driver.find_elements_by_css_selector("[class='review-comment']")
        # Get product review
        for product in product_reviews:
            review = product.find_element_by_css_selector("[class='review-comment__content']").text
            if (review != "" or review.strip()):
                print(review, "\n")
                list_review.append(review)
        #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        try:
            #driver.find_element_by_xpath("//li[@class='btn next']/a").click()
            button_next=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'btn next']")))
            driver.execute_script("arguments[0].click();", button_next)
            print("next page")
            time.sleep(2)
            x +=1
        except (TimeoutException, WebDriverException) as e:
            print('Load several page!')
            break
    driver.close()
    return list_review

# standardize data
def standardize_data(row):
    # remove stopword
    # Remove . ? , at index final
    row = re.sub(r"[\.,\?]+$-", "", row)
    # Remove all . , " ... in sentences
    row = row.replace(",", " ").replace(".", " ") \
        .replace(";", " ").replace("“", " ") \
        .replace(":", " ").replace("”", " ") \
        .replace('"', " ").replace("'", " ") \
        .replace("!", " ").replace("?", " ") \
        .replace("-", " ").replace("?", " ")

    row = row.strip()
    return row

# url = "https://tiki.vn/dien-thoai-samsung-galaxy-m31-128gb-6gb-hang-chinh-hang-p58259141.html"
# data = load_url_selenium_tiki(url)
# data = load_url_selenium_lazada(url)
# print (data)