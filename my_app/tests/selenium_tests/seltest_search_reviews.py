from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
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
        # Click the link with href="/recent_reviews"
        driver.find_element(By.CSS_SELECTOR, 'a[href="/recent_reviews"]').click()

        # Wait for page to load.
        time.sleep(5)

        # Select the input field and type "Miracle of life"
        review_search_input = driver.find_element(By.ID, 'review-search')
        review_search_input.clear()  # Clear any existing value
        review_search_input.send_keys("Miracle of life")

        time.sleep(5)

        print("Test complete for search!")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering login details: {e}")

except TimeoutException:
    print("Error: The page took too long to load.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
