from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Set up the web driver.
driver = webdriver.Chrome() 

try:

    # CREATING THE FIRST USER

    # Navigate to the sign-up page
    driver.get('http://localhost:5000/auth/signup')

    # Wait for the page to load
    time.sleep(2)

    # Enter test sign-up details
    try:
        # Locate the username field and enter a username
        username_field = driver.find_element(By.NAME, 'username')  # Adjust the selector as needed
        username_field.send_keys('testuser1')

        # Locate the email field and enter an email
        email_field = driver.find_element(By.NAME, 'email')  # Adjust the selector as needed
        email_field.send_keys('testuser@example.com')

        # Locate the password field and enter a password
        password_field = driver.find_element(By.NAME, 'password')  # Adjust the selector as needed
        password_field.send_keys('securepasswOrd123!')
        
        # Locate the password confirmation field and enter a password
        password_field = driver.find_element(By.NAME, 'confirm_password')  # Adjust the selector as needed
        password_field.send_keys('securepasswOrd123!')

        # Locate and click the sign-up button with the name "submit"
        submit_button = driver.find_element(By.NAME, 'submit')  # Adjust the selector as needed
        submit_button.click()

        time.sleep(5) # Wait for user creation confirmation prompt.

        print("Sign-up details entered and submitted successfully.")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering sign-up details: {e}")

    # Wait for the sign-up process to complete
    time.sleep(2)

    # CREATING THE SECOND USER

    # Navigate to the sign-up page
    driver.get('http://localhost:5000/auth/signup')

    # Wait for the page to load
    time.sleep(2)

    # Enter test sign-up details
    try:
        # Locate the username field and enter a username
        username_field = driver.find_element(By.NAME, 'username')  # Adjust the selector as needed
        username_field.send_keys('testuser2')

        # Locate the email field and enter an email
        email_field = driver.find_element(By.NAME, 'email')  # Adjust the selector as needed
        email_field.send_keys('testuser2@example.com')

        # Locate the password field and enter a password
        password_field = driver.find_element(By.NAME, 'password')  # Adjust the selector as needed
        password_field.send_keys('securepasswOrd123!')
        
        # Locate the password confirmation field and enter a password
        password_field = driver.find_element(By.NAME, 'confirm_password')  # Adjust the selector as needed
        password_field.send_keys('securepasswOrd123!')

        # Locate and click the sign-up button with the name "submit"
        submit_button = driver.find_element(By.NAME, 'submit')  # Adjust the selector as needed
        submit_button.click()

        time.sleep(5) # Wait for user creation confirmation prompt.

        print("Sign-up details entered and submitted successfully.")

    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")

    except Exception as e:
        print(f"An unexpected error occurred while entering sign-up details: {e}")

    # Wait for the sign-up process to complete
    time.sleep(2)

except TimeoutException:
    print("Error: The page took too long to load.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
