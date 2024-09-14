import re
from playwright.sync_api import Page
import string, random
import re
####### Help functions and classes
class Multi_check_box:
    def __init__(self, names: list[3], page: Page):
        self.names = names
        self.iframe = page.frame_locator("iframe")
        self.default_target_values = [True, False, False]
        self.check_states(self.default_target_values)

    def check_states(self, target_values: list[3]):
        for name, checked in zip(self.names, target_values):
            assert self.iframe.get_by_role('checkbox', name = name).is_checked() == checked, f"{name} is {checked}, should be {not checked}"

    def set_states(self, target_values: list[3]):
        for name, checked in zip(self.names, target_values):
            if checked == True:
                self.iframe.get_by_role('checkbox', name = name).check()
            elif checked == False:
                self.iframe.get_by_role('checkbox', name = name).uncheck()
            else:
                assert False, f"For writing was given wrong value {checked}, should be {True} or {False}"

    def check_output_list(self, target_values):
        output_name = "Checked names"
        output_text = self.iframe.get_by_text(output_name).inner_text()
        names_in_list = re.findall(r'\"(.*?)\"', output_text)
        target_list = [b for a, b in zip(target_values, self.names) if a]
        assert names_in_list == target_list, f'Names at the output list are {names_in_list}, should be {target_values}'        

def options_set_check_function(select, output, option_targets: list):
    for option_target in option_targets:
        select.select_option(option_target)
        option_readed = output.text_content()
        assert option_readed == f"Selected: {option_target}", f"Readed option was {option_readed}, should be {option_target}"

######## Tests

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

def test_multi_check_box(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    items_names = ['Jack', 'John', 'Mike']
    multi_check_box = Multi_check_box(items_names, page)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                target_values = [bool(i), bool(j), bool(k)]
                multi_check_box.set_states(target_values)
                multi_check_box.check_states(target_values)
                multi_check_box.check_output_list(target_values)

def test_radio(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    iframe = page.frame_locator("iframe")
    radio_button_one = iframe.get_by_role('radio', name = 'One')
    radio_button_two = iframe.get_by_role('radio', name = 'Two')
    radio_button_one.wait_for(state="visible")
    radio_button_two.wait_for(state="visible")
    picked_button_text = iframe.get_by_text('Picked')
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'One'
    radio_button_two.click()
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'Two'
    radio_button_one.click()
    assert (picked_button_text.text_content()).replace('Picked: ', '') == 'One'
    
def test_select(page: Page):
    page.goto("https://vuejs.org/examples/#form-bindings")
    iframe = page.frame_locator("iframe")
    select = iframe.locator('select').nth(0)
    output = iframe.get_by_text(re.compile(r'Selected: [ABC]'))
    options_list = ['A', 'B', 'C']
    options_set_check_function(select, output, options_list)








