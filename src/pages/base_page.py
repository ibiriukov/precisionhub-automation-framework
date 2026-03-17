from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page):
        self._page = page
        self.page_header = self.page.locator(".oxd-topbar-header-breadcrumb")
        self.user_dropdown_tab = self.page.locator(".oxd-userdropdown-tab")
        self.user_menu_items = self.page.locator(".oxd-dropdown-menu li")

    @property
    def page(self) -> Page:
        return self._page


    def get_header(self):
        self.wait_until_loaded()
        return self.page_header.text_content()

    def wait_until_loaded(self):
        self.page_header.wait_for(state="visible")

    def open_user_dropdown(self):
        self.user_dropdown_tab.click()
        self.user_menu_items.first.wait_for(state="visible")

    def click_user_menu_item(self, item_name: str):
        self.open_user_dropdown()
        self.page.get_by_role("menuitem", name=item_name).click()

