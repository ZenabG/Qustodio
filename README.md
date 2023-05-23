# Qustodio

This is a mobile android project created using **Appium Framework with Python**.

## Project Test Execution Steps:
1. Choose an IDE of your choice (Recommended : Pycharm)
2. Choose a path in your desktop to clone the git project and use `git clone https://github.com/ZenabG/Qustodio.git`
3. Now create a virtual environment to install all dependencies by setting Python interpreter in your IDE. (Note: you should have python installed in your machine to choose from)
4. Activate the virtual environment using the command `source venv/bin/activate` (for Linux/Mac) or `venv\Scripts\activate` (for Windows).
5. Now install the requirements (dependencies) using the command `pip install -r requirements.txt`
6. Adjust the device details in `test/resources/appium-config.json` by changing the device OS version and name. 
7. Make sure the Qustodio kids app is freshly installed on the device
8. Now run `pytest --alluredir=allure-results` to run the tests using pytest and generate an allure report with test run details and screenshots. The directory `allure-results` will be created automatically with this command if doesn't exist. 
9. Invoke the allure report on your desktop using the command `allure serve allure-results
`

## Project Structure

The project follows **Page object model** mechanism with **Page Factory**. **Pytest framework** is used for executing the tests.

The project hierarchy is ->

**pages** :
consists of 8 files for page methods and locators.

**setup** :
consists of Appium setup, start server and stop server

**test** - this folder stores json for appium desired caps under resources folder and Test class with 2 tests

