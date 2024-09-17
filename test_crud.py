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


class Button():
    def __init__(self, iframe, name: str):
        self.iframe = iframe
        self.name = name

    def click(self):
        iframe.get_by_role('button', name = self.name).click()

@pytest.fixture(scope="function")
def iframe(page: Page):
    """Fixture to set up and navigate to the modal example page"""
    page.goto("https://vuejs.org/examples/#crud")
    return page.frame_locator("iframe")

def test(iframe):
    crud = Crud(iframe)
    assert 1
