## Crud tests
## Author: Tomas Opletal

import re
from playwright.sync_api import Page
import string, random
import re
import pytest

names_list = ['Smith, John', 'Sevok, Emma', 'Brown, Michael', 'Williams, Olivia', 'Jones, David']

class Crud:
    """Base class which as members has all of the elements, which has lowest level funcionality (buttons, text windows, select window).
       Methods are implementing high level funcionality of crud (adding, deleting and rewritting options in select window, filtering, output text boxes)"""
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
        """Method used for checking default settings of the CRUD"""
        assert self.select_window.read_all_options() == ['Emil, Hans', 'Mustermann, Max', 'Tisch, Roman']
        assert self.name_window.read_text() == "", f"Name window should be empty"
        assert self.surname_window.read_text() == "", f"Surname window should be empty"
        assert self.filter_window.read_text() == "", f"Filter window should be empty"

    def options_labels_propagation_test(self):
        """Method for checking if is propagated text from the all options to the output text windows name and surname"""
        self.select_window.read_all_options()
        for i in range(self.select_window.number_options):
            self.select_window.click_option(i)
            assert self.surname_window.read_text() + ", " + self.name_window.read_text() == self.select_window.options[i]

    def add_option_to_select(self, names_list):
        """Method used for adding option/s to the select window. As argument it takes list of strings or one string"""
        if isinstance(names_list, str):
            names_list = [names_list]
        for full_name in names_list:
            number_options_prev = self.select_window.number_options
            options_prev = self.select_window.options
            surname, name = full_name.split(', ')
            self.name_window.click
            self.name_window.write(name)
            self.surname_window.click
            self.surname_window.write(surname)
            self.button_create.click()
            self.select_window.read_all_options()
            number_options_current = self.select_window.number_options
            options_current = self.select_window.options
            ## Checking adding elements in case adding already existing name - should be not added to the select
            if full_name in options_prev:
                assert options_prev == options_current
                assert number_options_current == number_options_prev
            ## Checking adding elements in case adding not existing name - should be added
            else:
                assert options_current[number_options_current - 1] == full_name, f"Was added {options_current[number_options_current]}, should be {full_name}"
                assert number_options_current == number_options_prev + 1, f"Currently is there {number_options_current}, should be {number_options_prev + 1}"

    def delete_option_from_select(self, names_list):
        """Method used for deleting element from the select option table. As argument takes list of strings or one string which should be removesd"""
        if isinstance(names_list, str):
            names_list = [names_list]
        for full_name in names_list:
            returned_index = self.select_window.find_option_by_name(full_name)
            number_options_prev = self.select_window.number_options
            if isinstance(returned_index, int):
                self.select_window.click_option(returned_index)
                self.button_delete.click()
                self.select_window.read_all_options()
                number_options_current = self.select_window.number_options
                # Checking if name and surname output text window are empty after delete
                assert self.name_window.read_text() == ''
                assert self.surname_window.read_text() == ''
                assert number_options_prev - 1 == number_options_current, f"Currently is there {number_options_current}, should be {number_options_prev - 1}"
                # Checking if there was no change in case not match between target name which should be deleted and current names in table.
            else:
                number_options_current = self.select_window.number_options
                assert number_options_prev == number_options_current, f"Some option was removes even though it shouldnt"
                continue

    def filter_options_by_name(self, filter: str):
        """Method used for filtering by name."""
        self.select_window.read_all_options()
        filtered_options_target = [name for name in self.select_window.options if name.startswith(filter)]
        self.filter_window.click()
        self.filter_window.write_text(filter)
        self.select_window.read_all_options()
        filtered_options_actual = self.select_window.options
        assert filtered_options_target == filtered_options_actual, f"Target filtered options was {filtered_options_target}, actual results is {filtered_options_actual}"

    def update_option_by_name(self, current_full_name, target_full_name):
        """Method used for update of existing name to another. As argument it takes current name, which should be overwritten by target name"""
        returned_index = self.select_window.find_option_by_name(current_full_name)
        if isinstance(returned_index, int):
            number_options_prev = self.select_window.number_options
            surname, name = target_full_name.split(', ')
            self.select_window.click_option(returned_index)
            self.name_window.click()
            self.name_window.write(name)
            self.surname_window.click()
            self.surname_window.write(surname)
            self.button_update.click()
            self.select_window.read_all_options()
            current_name = self.select_window.options[returned_index]
            number_options_current = self.select_window.number_options
            assert current_name == target_full_name, f"At the index {returned_index} is name {current_name}, should be {target_full_name}"
            assert number_options_current == number_options_prev, f"Number of options should be {number_options_prev}, should be {number_options_current}"
    

class Button():
    """Class button"""
    def __init__(self, iframe, name: str):
        self.iframe = iframe
        self.name = name

    def click(self):
        """Click method"""
        self.iframe.get_by_role('button', name = self.name).click()

class Label_Window():
    """Class label"""
    def __init__(self, iframe, text: str, nth):
        self.iframe = iframe
        self.name = text + ':'
        self.element = self.iframe.locator('label').nth(nth).locator('input')
    
    def read_text(self):
        """Method used for reading text"""
        return self.element.input_value()
    
    def click(self):
        """Method used for clicking this window """
        self.element.click()

    def write(self, text_to_write):
        """Method used for writting to this window"""
        self.element.fill(text_to_write)

class Filter_Window():
    """Class used for Filter window"""
    def __init__(self, iframe, text: str):
        self.iframe = iframe
        self.name = text
    
    def click(self):
        """Method used for clicking this window"""
        self.iframe.get_by_placeholder(self.name).click()
        
    def write_text(self, text: str):
        """Method used for writting to this window"""
        self.iframe.get_by_placeholder('Filter prefix').fill(text)
    
    def read_text(self):
        """Method used for reading this text which is in this window"""
        return self.iframe.get_by_placeholder('Filter prefix').input_value()

class Select_Window():
    """Class representing Select window"""
    def __init__(self, iframe):
        self.select_element = iframe.locator('select')
        self.options = []
        self.number_options = len(self.options)
        self.selected = None

    def read_all_options(self):
        """Method, which will read all current options and saves them to member variable"""
        self.select_element.locator('option').first.wait_for(state="visible")
        self.options = self.select_element.locator('option').all_inner_texts()
        self.number_options = len(self.options)
        return self.options
    
    def click_option(self, index):
        """Method used for clicking some concrete option by index"""
        self.select_element.locator('option').nth(index).click()
        self.selected = index
    
    def find_option_by_name(self, name):
        """Method used for finding option by name """
        self.read_all_options()
        for i, item in enumerate(self.options):
            if (name == item):
                return i
        return None

@pytest.fixture(scope="function")
def crud(page: Page):
    """Fixture to set up and navigate to the modal example page"""
    page.goto("https://vuejs.org/examples/#crud")
    page.wait_for_selector("iframe")
    iframe = page.frame_locator("iframe")
    crud = Crud(iframe)
    return crud

def test_default(crud):
    crud.check_default_setting()

def test_add_options_to_select(crud):
    crud.add_option_to_select(names_list[2:4])
    crud.add_option_to_select(names_list[2:4])

def test_options_labels_propagation(crud):
    crud.options_labels_propagation_test()

def test_delete_option_from_select(crud):
    crud.add_option_to_select(names_list[0:2])
    crud.delete_option_from_select([names_list[1:3]])

def test_filter_options_by_name(crud):
    crud.add_option_to_select(names_list)
    crud.filter_options_by_name("S")

def test_update_options_by_name(crud):
    crud.update_option_by_name(crud.select_window.options[0], names_list[1])
    crud.update_option_by_name(crud.select_window.options[1], names_list[2])








