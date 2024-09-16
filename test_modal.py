## Modal test
## Author: Tomas Opletal

import re
from playwright.sync_api import Page
import string, random
import re
import pytest

######## Fixtures

@pytest.fixture(scope="function")
def iframe(page: Page):
    """Fixture to set up and navigate to the modal example page"""
    page.goto("https://vuejs.org/examples/#modal")
    return page.frame_locator("iframe")

def test_modal(iframe):
    """Basic test for testing of modal funcionality"""
    button_show_modal = iframe.get_by_role('button', name = 'Show Modal')
    assert iframe.locator('div.modal-mask').is_hidden() == True
    button_show_modal.click()
    assert iframe.locator('div.modal-mask').is_visible() == True
    button_ok_modal = iframe.get_by_role('button', name = 'OK')
    header_name = 'Custom Header'
    body_name = 'default body'
    footer_name = 'default footer'
    assert iframe.locator('div.modal-header h3', has_text='Custom Header').text_content() == header_name
    assert iframe.locator('div.modal-body', has_text='default body').text_content() == body_name
    assert iframe.locator('div.modal-footer', has_text='default footer').inner_text() == footer_name + "\nOK"
    button_ok_modal.click()
    assert iframe.locator('div.modal-mask').is_hidden() == True
    



    
