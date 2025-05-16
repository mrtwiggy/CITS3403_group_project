import os

# Define the content
env_content = (
    "SECRET_KEY='your chosen secret key'\n"
    "WTF_CSRF_SECRET_KEY='your chosen secret key'\n"
)

# Define path to .env in the current working directory
env_path = os.path.join(os.getcwd(), ".env")

# Write the file
with open(env_path, "w") as env_file:
    env_file.write(env_content)

