# PrecisionHub Automation Framework

Enterprise-grade UI test automation framework built with:

- Python
- Pytest
- Playwright
- Page Object Model

---

## Project Structure
├── src/
│ ├── config/
│ │ settings.py
│ │
│ ├── pages/
│ │ base_page.py
│ │ login_page.py
│ │ dashboard_page.py
│ │
│ │ pim/
│ │ pim_page.py
│ │ add_employee_page.py
│ │ personal_details_page.py
│ │ employee_list_page.py
│ │
│ └── utils/
│ data_generators.py
│
├── tests/
│ ├── ui/
│ │ test_auth.py
│ │ test_pim_navigation.py
│ │ test_employee_crud.py
│ │
│ └── conftest.py
│
├── .env.example
├── pytest.ini
├── requirements.txt
├── README.md
│
└── .github/
workflows/
tests.yml