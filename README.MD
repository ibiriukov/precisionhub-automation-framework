# PrecisionHub Automation Framework

Demo automation framework showing how PrecisionHub structures scalable test automation across UI, API, and hybrid test layers.

Built with:

- Python
- Pytest
- Playwright
- Page Object Model
- GitHub Actions

---

## Key Capabilities

- UI automation with Playwright
- API testing with reusable client layer
- Hybrid UI + API validation
- Environment-based configuration with `.env` files
- Multi-browser support via configuration
- Screenshots and traces on failure
- Smoke execution in GitHub Actions

---

## Project Structure

```text
precisionhub-automation-framework/
├── .github/
│   └── workflows/
│       └── smoke.yml
├── src/
│   ├── api/
│   │   ├── client.py
│   │   └── users_api.py
│   ├── config/
│   │   └── settings.py
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── dashboard_page.py
│   └── utils/
├── tests/
│   ├── api/
│   │   └── test_users.py
│   └── ui/
│       ├── conftest.py
│       ├── test_auth.py
│       └── test_hybrid_api_ui.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt