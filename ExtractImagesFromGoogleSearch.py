import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import os


# Function to download the image and save it with a unique filename
def download_image(image_urls):
    i=0
    for image_url in image_urls:     
        save_path ="img"+str(i) + ".jpg"
        # Make a request to fetch the image content
        response = requests.get(image_url)
        if response.status_code == 200:
            # Write the content to a file
            with open(save_path, 'wb') as file:
                file.write(response.content)
            i+=1
            print(f"Image successfully downloaded and saved as {save_path}")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")

def get_image_from_url(title,numberOfImages):
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    # Navigate to the web page
    driver.get(f"https://www.google.com/search?q={title}&tbm=isch")
    # Hovering over the elements so we can get the href link in a tag , as have dynamic loading
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.H8Rx8c')  # Adjust the CSS selector as needed
    # Initialize ActionChains
    actions = ActionChains(driver)
    for element in elements[0:numberOfImages]:
        actions.move_to_element(element).perform()
    # Define the number of times to scroll
    scroll_count = 0 # if we need more values we can use this
    # Create an ActionChains object to perform the hover action
    actions = ActionChains(driver)
    # Simulate continuous scrolling using JavaScript
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0)  # Wait for the new results to load (adjust as needed)
    # Get the page source after scrolling
    page_source = driver.page_source
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    # Extract and print search results
    search_results = soup.find_all("h3", class_="ob5Hkd")
    driver.quit()
    links = []
    for result in search_results[0:numberOfImages]:
        a=result.find('a')
        if a:
            # print(a)
            href =a.get('href')
            if href:
                hrefimg = 'https://www.google.com'+href
                # print(hrefimg)

                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('window-size=1920x1080')
                driver = webdriver.Chrome(options=options)
                driver.get(hrefimg)
                elements = driver.find_elements(By.CSS_SELECTOR, 'div.p7sI2 PUxBg')  # Adjust the CSS selector as needed
                # Initialize ActionChains
                actions = ActionChains(driver)
                for element in elements:
                    actions.move_to_element(element).perform()
                page_source = driver.page_source
                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(page_source, "html.parser")
                imgdiv=soup.find('div',{'class':'p7sI2 PUxBg'})
                if imgdiv:
                    imgtag=imgdiv.find_all('img')
                    if imgtag:
                        for imgs in imgtag[0:1]:
                            link=imgs.get('src')
                            # calling image download function to dowbload image and to save
                            links.append(link)
                            print(link)
                    else:
                        print("no img tag found in p7sI2 PUxBg")
                else:
                    print("no such div found p7sI2 PUxBg")
                driver.quit()
            else:
                print("no href link found in a(for img)")
        else:
            print("a does not exist")
    download_image(links)

no=int(input("No. of images u want :"))
title = input("Enter the title for which u want images(url) :")
get_image_from_url(title , no)