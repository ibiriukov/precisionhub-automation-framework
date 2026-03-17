from playwright.sync_api import Page

from src.pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.quick_launch_widget = page.locator(
            "div.oxd-sheet.orangehrm-dashboard-widget"
        ).filter(
            has=page.locator("p", has_text="Quick Launch")
        )

        self.quick_launch_labels = self.quick_launch_widget.locator(
            ".orangehrm-quick-launch-heading p"
        )

    def wait_for_quick_launch(self) -> None:
        self.quick_launch_widget.wait_for(state="visible")
        self.quick_launch_labels.first.wait_for(state="visible")

    def get_shortcuts_count(self) -> int:
        self.wait_for_quick_launch()
        return self.quick_launch_labels.count()

    def get_shortcut_names(self) -> list[str]:
        self.wait_for_quick_launch()
        return [
            " ".join(text.split())
            for text in self.quick_launch_labels.all_inner_texts()
            if text.strip()
        ]

    def is_shortcut_visible(self, shortcut_name: str) -> bool:
        self.wait_for_quick_launch()
        locator = self.quick_launch_labels.filter(has_text=shortcut_name)
        return locator.count() > 0 and locator.first.is_visible()

    def debug_shortcuts(self) -> None:
        self.wait_for_quick_launch()
        print("Shortcut count:", self.get_shortcuts_count())
        print("Shortcut names:", self.get_shortcut_names())