import subprocess

# List of test modules to run
test_modules = [
    "my_app.tests.test_profilepic",
    "my_app.tests.test_friend",
    "my_app.tests.test_auth",
    "my_app.tests.test_review"
    
]

def run_tests():
    for test in test_modules:
        print(f"\nRunning test: {test}")
        result = subprocess.run(["python", "-m", test])
        if result.returncode != 0:
            print(f"❌ Test failed: {test}")
        else:
            print(f"✅ Test passed: {test}")

if __name__ == "__main__":
    run_tests()
