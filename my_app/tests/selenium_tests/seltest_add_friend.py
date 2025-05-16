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
        explore_link = driver.find_element(By.LINK_TEXT, 'Explore') 
        explore_link.click()

        print("Went to explore page successfully.")

        time.sleep(2) # Wait for explore page to load.

        user_search_field = driver.find_element(By.ID, 'user-search') 
        user_search_field.send_keys('testuser2')

        time.sleep(5) # Delay to wait for search results to display.

        friendship_button = driver.find_element(By.CLASS_NAME, 'friendship-btn')
        friendship_button.click()
        
        time.sleep(2) # Delay to process new friend.and

        print("Test passed! You now have requested to make a new friend! :)")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering adding friend: {e}")

except TimeoutException:
    print("Error: The page took too long to load.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
