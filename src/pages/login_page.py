from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.pages.dashboard_page import DashboardPage
from src.config.settings import BASE_URL

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_btn = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_text("Invalid credentials", exact=True)
        self.required_error = page.get_by_text("Required", exact=True)

    def open(self):
        self.page.goto(BASE_URL + "/web/index.php/auth/login")


    def login_success(self, username, password):
        self.submit_login(username, password)
        self.page.wait_for_url("**/dashboard/index")
        return DashboardPage(self.page)

    def submit_login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()

    def error_visible(self):
        self.error_message.wait_for(state="visible")
        return self.error_message.is_visible()

    def wait_until_loaded(self):
        self.username_input.wait_for(state="visible")

    def is_loaded(self):
        self.wait_until_loaded()
        return self.username_input.is_visible()

    def required_errors_count(self):
        self.required_error.first.wait_for(state="visible")
        return self.required_error.count()


