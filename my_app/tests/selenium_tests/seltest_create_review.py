from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time

# Set up the web driver (make sure the path to your driver is correct)
driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

try:
    # Navigate to the login page
    driver.get('http://localhost:5000/auth/login')  # Updated URL

    # Wait for the page to load
    time.sleep(2)  # You can use WebDriverWait for a more robust solution

    # Enter login details
    try:
        # Locate the email field and enter an email
        email_field = driver.find_element(By.NAME, 'email') 
        email_field.send_keys('testuser@example.com')

        # Locate the password field and enter a password
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys('securepasswOrd123!')

        # Locate and click the login button with the name "submit"
        submit_button = driver.find_element(By.NAME, 'submit') 
        submit_button.click()

        print("Login details entered and submitted successfully.")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering login details: {e}")

    
    time.sleep(2) # Wait for the login process to complete.

    # After logging in.

    try:
        # Selecting creating review page.
        review_link = driver.find_element(By.XPATH, "//a[@href='/review/reviews']")
        review_link.click()
        print("Clicked the review hyperlink successfully.")

    except NoSuchElementException:
        print("Error: Review hyperlink not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the hyperlink: {e}")

    # Wait for the new page to load.
    time.sleep(2)

    # Click the dropdown menu with the name "franchise_id".
    try:
        franchise_dropdown = driver.find_element(By.NAME, 'franchise_id')
        franchise_dropdown.click()
        print("Clicked the franchise dropdown successfully.")

    except NoSuchElementException:
        print("Error: Franchise dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    # Wait for a moment to see the result.
    time.sleep(2)

    try:
        # Select random option from the dropdown.
        select = Select(franchise_dropdown)
        options = select.options
        random_store = random.randint(1, len(options) - 1)
        select.select_by_index(random_store)

        print(f"[FRANCHISE] Selected option {random_store} out of {len(options)} options in the dropdown successfully.")

        time.sleep(2)
    
    except TimeoutException:
        print("Error: The page took too long to load.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Deselect the dropdown menu.
    try:
        franchise_dropdown = driver.find_element(By.NAME, 'franchise_id')
        franchise_dropdown.click()
        print("Clicked the franchise dropdown successfully.")

        time.sleep(2)

    except NoSuchElementException:
        print("Error: Franchise dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    # Handling location selection.

    # Click the dropdown menu with the name "location_id".
    try:
        location_dropdown = driver.find_element(By.NAME, 'location_id')
        location_dropdown.click()
        print("Clicked the location dropdown successfully.")

    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    # Wait for a moment to see the result.
    time.sleep(2)

    try:
        # Select random option from the dropdown.
        select = Select(location_dropdown)
        options = select.options
        random_location = random.randint(1, len(options) - 1)
        select.select_by_index(random_location)

        print(f"[LOCATION] Selected option {random_location} out of {len(options)} options in the dropdown successfully.")

        time.sleep(2)
    
    except TimeoutException:
        print("Error: The page took too long to load.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Deselect the dropdown menu.
    try:
        location_dropdown = driver.find_element(By.NAME, 'location_id')
        location_dropdown.click()
        print("Clicked the franchise dropdown successfully.")

        time.sleep(2)

    except NoSuchElementException:
        print("Error: Franchise dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")
    
    try: 
        # Put drink name.
        drink_name_input = driver.find_element(By.NAME, 'drink_name')
        drink_name_input.clear()
        drink_name_input.send_keys("Miracle of life")

        # Select a random drink size.
        drink_size_options = driver.find_elements(By.NAME, 'drink_size')
        if drink_size_options:
            random.choice(drink_size_options).click()

        time.sleep(2)

    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    try:
        # Put sugar and ice levels.

        # Sugar levels first.
        sugar_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-group="sugar"]')
        if sugar_buttons:
            random.choice(sugar_buttons).click()
        
        time.sleep(2)

        # Then ice levels.
        ice_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-group="ice"]')
        if ice_buttons:
            random.choice(ice_buttons).click()

            time.sleep(2)

    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    try: 
        # Put drink review.
        drink_review_input = driver.find_element(By.NAME, 'review_content')
        drink_review_input.clear()
        drink_review_input.send_keys("""This thing saved my life.


It cured all my illnesses. It was so powerful it literally GAVE me cancer JUST TO CURE IT AGAIN! It also gave me the answer to the meaning of literally everything which I can't tell anyone for reasons that I also can't tell anyone.


TL;DR - Changed my life for the better. :)""")

        time.sleep(2)

    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    try:
        # Rate drink and choose privacy settings.

        # Rating drink.
        rating_stars = driver.find_elements(By.CSS_SELECTOR, '#boba-rating span')
        if rating_stars:
            random.choice(rating_stars).click()

        time.sleep(2)

        # Select a random option from the privacy dropdown.
        options = driver.find_elements(By.CSS_SELECTOR, '#privacy-select option')
        random.choice(options).click()

        time.sleep(2)
        
    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    try:
        # Submit review.
        driver.find_element(By.NAME, 'submit').click()

        time.sleep(5)
    
    except NoSuchElementException:
        print("Error: Location dropdown not found.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking the dropdown: {e}")

    print("You have successfully reviewed a drink! Hope it changed your life! ;) I hope you didn't randomly rate it now LOL. O___O")

except TimeoutException:
    print("Error: The page took too long to load.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
