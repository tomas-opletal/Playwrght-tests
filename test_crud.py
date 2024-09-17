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
        self.iframe = iframe
        self.button_Create = Button(self.iframe, 'Create')
        self.button_Update = Button(self.iframe, 'Update')
        self.button_Delete = Button(self.iframe, 'Delete')
        self.name_window = Label_Window(self.iframe, 'Name')
        self.surname_window = Label_Window(self.iframe, 'Surname')
        self.filter_window = Filter_Window(self.iframe, 'Filter prefix')
        self.output_window = Output_Window(self.iframe)

class Button():
    def __init__(self, iframe, name: str):
        self.iframe = iframe
        self.name = name

    def click(self):
        iframe.get_by_role('button', name = self.name).click()

class Label_Window():
    def __init__(self, iframe, text: str):
        self.iframe = iframe
        self.name = text + ':'
    
    def read_text(self):
        return iframe.locator('label', has_text = self.name).locator('input')

class Filter_Window():
    def __init__(self, iframe, text: str):
        self.iframe = iframe
        self.name = text
    
    def click(self):
        self.iframe.get_by_placeholder(self.name).click()
        
    def write_text(self, text: str):
        self.iframe.get_by_placeholder('Filter prefix').fill(text)
    
    def read_text(self):
        return self.iframe.get_by_placeholder('Filter prefix').inner_text()

class Output_Window():
    def __init__(self, iframe):
        self.select_element = iframe.locator('select')
        self.options = []

    def read_all_options(self):
        self.options = self.select_element.locator('option').all_inner_texts()
        return self.options
    

@pytest.fixture(scope="function")
def iframe(page: Page):
    """Fixture to set up and navigate to the modal example page"""
    page.goto("https://vuejs.org/examples/#crud")
    return page.frame_locator("iframe")

def test(iframe, name_to_write):
    crud = Crud(iframe)
    iframe.get_by_placeholder('Filter prefix').all_inner_texts()
    assert 1
