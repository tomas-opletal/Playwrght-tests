import re
from playwright.sync_api import Page, expect
import string, random

def test_has_title(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    assert page.title() == "Examples | Vue.js"

def test_text_box(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    testing_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    text_input = page.frame_locator("iframe").get_by_role("textbox")
    text_input.click()
    text_input.fill(f"{testing_string}")
    assert text_input.input_value() == (f"{testing_string}")

def test_check_box(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    check_box = page.frame_locator("iframe").get_by_role("checkbox", name= "Checked:")
    assert check_box.is_checked() == True, f"Checkbox is {check_box.is_checked()}, should be True"
    check_box.uncheck()
    assert check_box.is_checked() == False, f"Checkbox is {check_box.is_checked()}, should be False"


    

