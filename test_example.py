import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")

    # Expect a title "to contain" a substring.
    assert page.title() == "Examples | Vue.js"

