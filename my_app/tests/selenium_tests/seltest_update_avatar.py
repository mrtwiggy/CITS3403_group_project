from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
        email_field = driver.find_element(By.NAME, 'email')  # Adjust the selector as needed
        email_field.send_keys('testuser@example.com')

        # Locate the password field and enter a password
        password_field = driver.find_element(By.NAME, 'password')  # Adjust the selector as needed
        password_field.send_keys('securepasswOrd123!')

        # Locate and click the login button with the name "submit"
        submit_button = driver.find_element(By.NAME, 'submit')  # Adjust the selector as needed
        submit_button.click()

        print("Login details entered and submitted successfully.")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering login details: {e}")

    
    time.sleep(2) # Wait for the login process to complete.

    # After logging in.

    try:
        
        # Locate the button with the text "Change Avatar" and click it.
        change_avatar_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Change Avatar')]")
        change_avatar_button.click()

        time.sleep(2) # Wait for avatar options to load.

        # Locate the image with alt text "Avatar X" (random avatar!) and click it.
        random_avatar = random.randint(1, 9)
        print(f"Picked random avatar number: {random_avatar}! What do you think? A good choice?")
        
        avatar_image = driver.find_element(By.XPATH, f"//img[@alt='Avatar {random_avatar}']")
        avatar_image.click()

        time.sleep(2) # Delay for selection.

        # Locate the button with the text "Save Changes" and click it.
        save_changes_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save Changes')]")
        save_changes_button.click()

        time.sleep(5) # Delay to acknowledge the shock of your cool new outfit!

        print("Test successful! You now have a cool new look!")

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
