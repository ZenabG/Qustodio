import random

import allure
import pytest
import os

from pages.AvatarPage import AvatarPage
from pages.ChildDetailsPage import ChildDetailsPage
from pages.DeviceNamePage import DeviceNamePage
from pages.DeviceSettingsPage import DeviceSettingsPage
from pages.GetStartedPage import GetStartedPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from pages.WelcomePage import WelcomePage
from setup import AppiumSetUp


class PageObjects:
    def __init__(self, driver):
        self.home_page = HomePage(driver)
        self.get_started_page = GetStartedPage(driver)
        self.login_page = LoginPage(driver)
        self.welcome_page = WelcomePage(driver)
        self.device_name_page = DeviceNamePage(driver)
        self.child_details_page = ChildDetailsPage(driver)
        self.avatar_page = AvatarPage(driver)
        self.device_settings_page = DeviceSettingsPage(driver)


random_number = random.randint(10000, 20000)
test_user_name = "Test User"
test_user_email = "test19716@qustodio.com"
test_user_password = "123456"
welcome_user = "Welcome, Test User!"
device_name = "Galaxy tab"
child_name = "Danu"
toggle_settings = "Qustodio Kids"


@pytest.fixture(scope="function")
def set_up():
    appium_process = AppiumSetUp.start_appium_server()
    driver = AppiumSetUp.appium_driver(_get_appium_config_path())
    yield driver
    AppiumSetUp.stop_appium_server(appium_process)


@allure.description("New user registration flow test")
def test_get_started_page_flow(set_up):
    driver = set_up
    # initialise page objects with webdriver
    page_objects = PageObjects(driver)

    # New user registration flow
    page_objects.home_page.click_get_started_button()
    test_email = "test" + str(random_number) + "@qustodio.com"
    page_objects.get_started_page.enter_user_details(test_user_name, test_user_password,
                                                     test_email)

    _capture_screenshot(driver, "User registration form")
    page_objects.get_started_page.accept_privacy_policy()
    page_objects.get_started_page.click_submit_button()
    assert page_objects.welcome_page.get_welcome_text() == welcome_user

    _capture_screenshot(driver, "Assert Welcome User page")


@allure.description("Protect this device flow with freshly installed app and existing user account and child")
def test_allow_all_protect_device(set_up):
    driver = set_up
    # initialise page objects with webdriver
    page_objects = PageObjects(driver)

    # login with existing user
    page_objects.home_page.click_login_button()
    page_objects.login_page.user_login(test_user_email, test_user_password)
    assert page_objects.welcome_page.get_welcome_text() == welcome_user

    _capture_screenshot(driver, "User log in")

    # start protect this device flow
    page_objects.welcome_page.click_protect_this_device()

    _capture_screenshot(driver, "Click on protect this device button")

    # enter device name (using existing device name here and accepting replace alert as only 3 devices allowed per user)
    page_objects.device_name_page.enter_device_name(device_name)
    page_objects.device_name_page.click_next()

    _capture_screenshot(driver, "Enter device name")

    # using existing child as gender dropdown doesn't have locators to chose
    page_objects.child_details_page.pick_existing_child(child_name)

    _capture_screenshot(driver, "Pick an existing child")

    # click Let's do it button
    page_objects.device_settings_page.lets_do_it_button()

    _capture_screenshot(driver, "Click on 'Let's do it' button")

    # Allow accessibility access
    page_objects.device_settings_page.allow_accessibility_tracking()

    _capture_screenshot(driver, "Allow accessibility tracking")

    # Allow usage tracking
    page_objects.device_settings_page.allow_usage_tracking(toggle_settings)

    _capture_screenshot(driver, "Allow usage tracking")

    # Allow notification access
    page_objects.device_settings_page.allow_notification_access(toggle_settings)

    _capture_screenshot(driver, "Allow notification access")

    # Allow app display
    page_objects.device_settings_page.allow_app_display(toggle_settings)

    _capture_screenshot(driver, "Allow app display")

    # Allow additional permissions
    page_objects.device_settings_page.allow_permissions()

    _capture_screenshot(driver, "Allow other permissions")

    # Activate device admin
    page_objects.device_settings_page.activate_device_admin()

    _capture_screenshot(driver, "Activate device admin")

    # Assert Finish button on done page
    assert page_objects.device_settings_page.is_qustodio_protection_enabled() == True

    _capture_screenshot(driver, "Assert Finish button is present")


def _get_appium_config_path():
    project_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_directory, "resources/appium_config.json")


def _capture_screenshot(driver, screenshot_name):
    allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
                  attachment_type=allure.attachment_type.PNG)
