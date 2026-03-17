import time

import pytest

from src.config.settings import BASE_URL


API_TO_UI_SHORTCUTS = {
    "leave.assign_leave": "Assign Leave",
    "leave.leave_list": "Leave List",
    "leave.apply_leave": "Apply Leave",
    "leave.my_leave": "My Leave",
    "time.employee_timesheet": "Timesheets",
    "time.my_timesheet": "My Timesheet",
}


def get_dashboard_shortcut_flags(dashboard_page):
    #dashboard_page.quick_launch_widget.wait_for()
    resp = dashboard_page.page.request.get(
        f"{BASE_URL}/web/index.php/api/v2/dashboard/shortcuts"
    )
    assert resp.status == 200, f"Unexpected status code: {resp.status}"

    payload = resp.json()
    assert "data" in payload, f"Missing 'data' in response: {payload}"
    assert isinstance(payload["data"], dict), (
        f"'data' should be dict, got: {type(payload['data']).__name__}"
    )

    return payload["data"]


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.regression
def test_quick_launch_count_matches_enabled_api_flags(dashboard_page):
    shortcut_flags = get_dashboard_shortcut_flags(dashboard_page)

    expected_count = sum(
        1 for api_key in API_TO_UI_SHORTCUTS if shortcut_flags.get(api_key, False)
    )
    actual_count = dashboard_page.get_shortcuts_count()

    assert actual_count == expected_count, (
        f"Quick Launch count mismatch. "
        f"Expected from API: {expected_count}, actual in UI: {actual_count}"
    )


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.regression
def test_quick_launch_names_match_enabled_api_flags(dashboard_page):
    shortcut_flags = get_dashboard_shortcut_flags(dashboard_page)

    expected_names = sorted(ui_name for api_key, ui_name in API_TO_UI_SHORTCUTS.items() if shortcut_flags.get(api_key, False))
    actual_names = sorted(dashboard_page.get_shortcut_names())

    assert actual_names == expected_names, (
        f"Quick Launch names mismatch.\n"
        f"Expected from API: {expected_names}\n"
        f"Actual in UI: {actual_names}"
    )


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(("api_key", "ui_name"), API_TO_UI_SHORTCUTS.items())
def test_each_quick_launch_item_visibility_matches_api_flag(
    dashboard_page, api_key, ui_name
):
    dashboard_page.wait_for_quick_launch()

    shortcut_flags = get_dashboard_shortcut_flags(dashboard_page)

    expected_visible = shortcut_flags.get(api_key, False)
    actual_visible = dashboard_page.is_shortcut_visible(ui_name)

    dashboard_page.debug_shortcuts()
    print(f"Checking: {ui_name}")
    print(f"Actual visible: {actual_visible}")

    assert actual_visible == expected_visible, (
        f"Visibility mismatch for '{ui_name}' ({api_key}). "
        f"Expected from API: {expected_visible}, actual in UI: {actual_visible}"
    )