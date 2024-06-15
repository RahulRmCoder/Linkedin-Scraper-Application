import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from linkedin_scraper import actions
from selenium.webdriver.chrome.service import Service

def scrape_person(linkedin_url):
    # Initialize WebDriver with Service object
    service = Service("C:/Users/ACER/Downloads/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # LinkedIn login
    email = ""
    password = ""
    actions.login(driver, email, password)  # Login to LinkedIn
    time.sleep(30)

    # Navigate to the LinkedIn profile URL
    driver.get(linkedin_url)

    # Wait for the profile to load
    time.sleep(10)  # Adjust this wait time as needed

    # Scrape name
    try:
        name_element = driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
        name = name_element.find_element(By.TAG_NAME, "h1").text
    except NoSuchElementException:
        name = "Name not available"

    # Scrape headline
    try:
        headline_element = driver.find_element(By.CLASS_NAME, "text-body-medium.break-words")
        headline = headline_element.text.strip()
    except NoSuchElementException:
        headline = "Headline not available"

    # Scrape location
    try:
        location = name_element.find_element(By.XPATH, "//*[@class='text-body-small inline t-black--light break-words']").text
    except NoSuchElementException:
        location = "Location not available"

    # Scrape number of connections
    try:
        connections = driver.find_element(By.CLASS_NAME, "t-bold").text
    except NoSuchElementException:
        connections = "Number of connections not available"

    # Scrape about section
    try:
        about = driver.find_element(By.ID, "about").find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "display-flex").text
    except NoSuchElementException:
        about = "About section not available"

    # Navigate to the skills section
    skills_url = linkedin_url + "details/skills/"
    driver.get(skills_url)

    # Wait for the skills page to load
    time.sleep(10)  # Adjust this wait time as needed

    height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break
        height = new_height

    # Scrape skills section
    try:
        skills_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
        skills = []
        for element in skills_elements:
            skill = element.find_element(By.CLASS_NAME, "visually-hidden").text
            skills.append(skill)
    except NoSuchElementException:
        skills = ["Skills not available"]

    # Print the scraped information
    print("Name:", name)
    print("Headline:", headline)
    print("Location:", location)
    print("Number of Connections:", connections)
    print()
    print("About:", about)
    print()
    print("\nSkills:")
    j = 1
    for i in skills:
        if i == "":
            break
        print(f'{j}.{i}')
        j += 1

    # Close the WebDriver
    driver.quit()

    data_to_save = f"Name: {name}\nHeadline: {headline}\nLocation: {location}\nNumber of Connections: {connections}\n\nAbout: {about}\n\nSkills:\n"
    for idx, skill in enumerate(skills, start=1):
        if skill == "":
            break
        data_to_save += f"{idx}. {skill}\n"

    # Write data to a text file
    file_name = f"{name}_linkedin_profile.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(data_to_save)

    print(f"Scraped data saved to {file_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        linkedin_url = sys.argv[1]
        scrape_person(linkedin_url)
    else:
        print("No LinkedIn URL provided.")
