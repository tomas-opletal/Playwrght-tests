## Form Bindings tests
## Author: Tomas Opletal

import re
from playwright.sync_api import Page
import string, random
import re
import pytest

####### Help functions and classes
class Multi_check_box:
    def __init__(self, names: list[3], page: Page):
        """Class which is used for testing of Multi check box element"""
        self.names = names
        self.iframe = page.frame_locator("iframe")
        self.default_target_values = [True, False, False]
        self.check_states(self.default_target_values) # Checking default value

    def check_states(self, target_values: list[3]):
        """Method used for checking of states of checks. It takes as argument target values"""
        for name, checked in zip(self.names, target_values):
            assert self.iframe.get_by_role('checkbox', name = name).is_checked() == checked, f"{name} is {checked}, should be {not checked}"

    def set_states(self, target_values: list[3]):
        """Method uset for setting of states of the checks. It takes as argument target values. Also check if they are in allowed range """
        for name, checked in zip(self.names, target_values):
            if checked == True:
                self.iframe.get_by_role('checkbox', name = name).check()
            elif checked == False:
                self.iframe.get_by_role('checkbox', name = name).uncheck()
            else:
                assert False, f"For writing was given wrong type value {checked}, should be {True} or {False}"

    def check_output_list(self, target_values):
        """Method used for checking of text which is inside output element."""
        output_name = "Checked names"
        output_text = self.iframe.get_by_text(output_name).inner_text()
        names_in_list = re.findall(r'\"(.*?)\"', output_text)
        target_list = [b for a, b in zip(target_values, self.names) if a]
        assert names_in_list == target_list, f'Names at the output list are {names_in_list}, should be {target_values}'        

class Multi_select:
    """Class which is used for testing of Multi select element."""
    def __init__(self, select_element, output_element) -> None:
        """As init values it takes select element and output element"""
        self.select_element = select_element
        self.output_element = output_element 

    def set_options(self, target_options: list):
        """Method uset for setting target options"""
        self.select_element.select_option(target_options)

    def check_options(self, target_options: list):
        """Method uset for checking the options"""
        readed_options = self.output_element.inner_text().replace("Selected: ", "")
        cleaned_str = readed_options.replace('[', '').replace(']', '').replace('"', '').strip() # Needed because readed string was in format '[ "A", "B", "C" ]'
        readed_options_cleaned = [letter.strip() for letter in cleaned_str.split(',')]
        if readed_options_cleaned == ['']:
            readed_options_cleaned = []
        assert readed_options_cleaned == target_options, f"Readed options was {readed_options_cleaned}, should be {target_options}"

def options_set_check_function(select, output_element, option_targets: list):
    """Function used for setting and checking options"""
    default_option_readed = output_element.text_content()
    assert default_option_readed == f"Selected: A", f"Readed option was {default_option_readed}, should be A" # Checking default option
    for option_target in option_targets:
        select.select_option(option_target)
        option_readed = output_element.text_content()
        assert option_readed == f"Selected: {option_target}", f"Readed option was {option_readed}, should be {option_target}"

######## Fixtures

@pytest.fixture(scope="function")
def page(page: Page):
    """Fixture to set up and navigate to the form bindings example page"""
    page.goto("https://vuejs.org/examples/#form-bindings")
    return page

######## Tests

def test_has_title(page):
    """Basic test for testing name of page"""
    assert page.title() == "Examples | Vue.js"

def test_text_box(page):
    """Test which is testing writting text to the text box and checking if this value is also set at output box"""
    test_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    text_input = page.frame_locator("iframe").get_by_role("textbox")
    default_output_target = "Edit me"
    readed_output_element = text_input.input_value()
    assert readed_output_element == default_output_target, f"Readed output was {readed_output_element}, should be {default_output_target}"
    text_input.click()
    text_input.fill(f"{test_string}")
    readed_output_element = text_input.input_value()
    assert readed_output_element == (f"{test_string}"), f"Readed output was {readed_output_element}, should be {test_string}" 

def test_check_box(page):
    """Test which s testing check box element"""
    check_box_element = page.frame_locator("iframe").get_by_role("checkbox", name= "Checked:")
    assert check_box_element.is_checked() == True, f"Checkbox is {check_box_element.is_checked()}, should be True"
    check_box_element.uncheck()
    assert check_box_element.is_checked() == False, f"Checkbox is {check_box_element.is_checked()}, should be False"

def test_multi_check_box(page):
    """"Test which is testing multi check box elements. Created class which encapsulate the funcionality."""
    items_names = ['Jack', 'John', 'Mike']  
    multi_check_box = Multi_check_box(items_names, page)
    # Logic which is testing all of the possible combination of items_names
    for i in range(2):
        for j in range(2):
            for k in range(2):
                target_values = [bool(i), bool(j), bool(k)]
                multi_check_box.set_states(target_values)
                multi_check_box.check_states(target_values)
                multi_check_box.check_output_list(target_values)

def test_radio(page):
    """Test for testing radio element"""
    iframe = page.frame_locator("iframe")
    radio_element_one = iframe.get_by_role('radio', name = 'One')
    radio_element_two = iframe.get_by_role('radio', name = 'Two')
    radio_element_one.wait_for(state="visible")
    radio_element_two.wait_for(state="visible")
    picked_button_text = iframe.get_by_text('Picked')
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'One' # Testing of default value
    radio_element_two.click()
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'Two' # Testing of clicking on the second button
    radio_element_one.click()
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'One' # Testing of clicking on the first button
    
def test_select(page):
    """Test for testing select element"""
    iframe = page.frame_locator("iframe")
    select_element = iframe.locator('select').nth(0)
    output_element = iframe.get_by_text(re.compile(r'Selected: [ABC]'))
    options_list = ['A', 'B', 'C']
    options_set_check_function(select_element, output_element, options_list)

def test_multi_select(page):
    """Test for testing multi select element"""
    iframe = page.frame_locator("iframe")
    select_element = iframe.locator('select').nth(1)
    output_element = iframe.locator('p', has_text= 'Selected: [')
    multi_select = Multi_select(select_element, output_element)
    option_list = ["A", "B", "C"]
    # Logic used for testing all of the combinations possible in multi select
    for i in range(2):
        for j in range(2):
            for k in range(2):
                option_bool_list = [bool(i), bool(j), bool(k)]
                target_list = [b for a, b in zip(option_bool_list, option_list) if a]
                multi_select.set_options(target_list)
                multi_select.check_options(target_list)









