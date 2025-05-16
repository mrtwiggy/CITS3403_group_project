import os
from my_app import create_app
from config import DeploymentConfig, TestConfig

# Determine which config to use based on environment variable
if os.environ.get('FLASK_ENV') == 'testing':
    app = create_app(TestConfig)
else:
    app = create_app(DeploymentConfig)

if __name__ == "__main__":
    app.run(debug=DeploymentConfig.DEBUG if 'DEBUG' in dir(DeploymentConfig) else False)