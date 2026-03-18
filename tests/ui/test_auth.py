
import pytest
from src.config.settings import BASE_URL
from src.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(dashboard_page):
    assert dashboard_page.get_header() == "Dashboard"

@pytest.mark.ui
@pytest.mark.regression
def test_login_invalid(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.submit_login("wrongUsername", "wrongPassword")
    assert login_page.error_visible()

@pytest.mark.ui
@pytest.mark.regression
def test_logout(dashboard_page):
    dashboard_page.click_user_menu_item("Logout")
    login_page = LoginPage(dashboard_page.page)
    assert login_page.is_loaded()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("username,password,expected", [
    ("","", 2),
    ("","somePassword", 1),
    ("someUsername", "", 1)])

def test_multiple_negative_scenarios(page,username,password,expected):
    login_page = LoginPage(page)
    login_page.open()
    login_page.submit_login(username, password)
    assert login_page.required_errors_count() == expected

@pytest.mark.ui
@pytest.mark.regression
def test_dashboard_requires_auth(page):
    page.goto(BASE_URL+"/web/index.php/dashboard/index")
    login_page = LoginPage(page)
    assert login_page.is_loaded()

@pytest.mark.ui
@pytest.mark.regression
def test_refresh_after_logout(dashboard_page):
   dashboard_page.click_user_menu_item("Logout")
   dashboard_page.page.reload()
   login_page = LoginPage(dashboard_page.page)
   assert not login_page.is_loaded()





