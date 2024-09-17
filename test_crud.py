## Crud tests
## Author: Tomas Opletal

import re
from playwright.sync_api import Page
import string, random
import re
import pytest


######## Fixtures

class Crud:
    def __init__(self, iframe):
        self._iframe = iframe
        self.button_create = Button(self._iframe, 'Create')
        self.button_update = Button(self._iframe, 'Update')
        self.button_delete = Button(self._iframe, 'Delete')
        self.name_window = Label_Window(self._iframe, 'Name', 0)
        self.surname_window = Label_Window(self._iframe, 'Surname', 1)
        self.filter_window = Filter_Window(self._iframe, 'Filter prefix')
        self.select_window = Select_Window(self._iframe)
        self.check_default_setting()
    
    def check_default_setting(self):
        assert self.select_window.read_all_options() == ['Emil, Hans', 'Mustermann, Max', 'Tisch, Roman']
        for i in range(self.select_window.number_options):
            assert self.select_window.is_checked_option(i) == False, f"Option {i} is checked, should be {False}"
        assert self.name_window.read_text() == "", f"Name window should be empty"
        assert self.surname_window.read_text() == "", f"Surname window should be empty"
        assert self.filter_window.read_text() == "", f"Filter window should be empty"



class Button():
    def __init__(self, iframe, name: str):
        self.iframe = iframe
        self.name = name

    def click(self):
        self.iframe.get_by_role('button', name = self.name).click()

class Label_Window():
    def __init__(self, iframe, text: str, nth):
        self.iframe = iframe
        self.name = text + ':'
        self.element = self.iframe.locator('label').nth(nth).locator('input')
    
    def read_text(self):
        return self.element.input_value()
    
    def click(self):
        self.element.click()

    def write(self, text_to_write):
        self.element.fill(text_to_write)

class Filter_Window():
    def __init__(self, iframe, text: str):
        self.iframe = iframe
        self.name = text
    
    def click(self):
        self.iframe.get_by_placeholder(self.name).click()
        
    def write_text(self, text: str):
        self.iframe.get_by_placeholder('Filter prefix').fill(text)
    
    def read_text(self):
        return self.iframe.get_by_placeholder('Filter prefix').input_value()

class Select_Window():
    def __init__(self, iframe):
        self.select_element = iframe.locator('select')
        self.options = []
        self.number_options = len(self.options)
        self.selected = None

    def read_all_options(self):
        self.options = self.select_element.locator('option').all_inner_texts()
        self.number_options = len(self.options)
        return self.options
    
    def click_option(self, index):
        self.select_element.locator('option').nth(index).click()
        self.selected = index

    def is_visible_option(self, index):
        return self.select_element.locator('option').nth(index).is_visible()
    
    def is_checked_option(self, index):
        return self.select_element.locator('option').nth(index).is_checked()


    


@pytest.fixture(scope="function")
def iframe(page: Page):
    """Fixture to set up and navigate to the modal example page"""
    page.goto("https://vuejs.org/examples/#crud")
    return page.frame_locator("iframe")

def test(iframe):
    crud = Crud(iframe)
    





