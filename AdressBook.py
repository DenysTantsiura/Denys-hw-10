'''Task 9 + 10
Bot. A console bot helper that will recognize commands entered 
from the keyboard and respond accordingly.
The bot accepts commands:
"hello", replies to the console "How can I help you?"
"add ...". With this command, the bot saves a new contact in memory. Instead of ... the user enters the name and phone number, necessarily with a space.
"change ..." With this command, the bot stores the new phone number of the existing contact in memory. Instead of ... the user enters the name and phone number, necessarily with a space.
"phone ...." With this command, the bot outputs the phone number for the specified contact to the console. Instead of ... the user enters the name of the contact whose number should be displayed.
"show all". With this command, the bot outputs all saved contacts with phone numbers to the console.
"good bye", "close", "exit" by any of these commands, the bot ends its work after outputting "Good bye!" to the console.
And from 10:
All classes from the task have been implemented.
Record entries in AddressBook are stored as values in a dictionary. Record.name.value is used as keys.
Record stores the Name object in a separate attribute.
Record stores a list of Phone objects in a separate attribute.
Record implements methods for adding/removing/editing Phone objects.
AddressBook implements the add_record method, which adds a Record to self.data.

"add phone ..." With this command, the bot saves a new phones to an existing contact record in memory. Instead of ... the user enters the name and phone number(s), necessarily with a space.'''

from collections import UserDict
import re
# import os
# import pickle


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record


class Field:  # super for all fields ... for the future
    pass


class Name(Field):
    def __init__(self, value):
        # super().__init__(name) ... for the future
        self.value = value


class Phone(Field):
    def __init__(self, value):
        # super().__init__(phone) ... for the future
        self.value = value


class Record():  # add remove change  field

    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = []
        if phones:
            for phone in phones:
                self.add_phone(phone)

    def add_phone(self, phone_new):
        self.phones.append(Phone(phone_new))

    def remove_phone(self, phone_to_remove):
        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                break

    def change_phone(self, phone_to_change, phone_new):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_change:
                self.phones.insert(index, Phone(phone_new))
                self.phones.remove(phone)
                break


contact_dictionary = AddressBook()


def validation_add(user_command, number_format, name):
    if len(user_command) < 2:
        return "Give me name OR name and phone please\n"
    if name in contact_dictionary:
        return "Such an entry is already in the book. Add or change a number."
    if name[0].isdigit():
        return "A name cannot begin with a number!\n"
    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"
    if len(user_command) >= 2:
        for phone_candidate in user_command[2:]:
            if not re.search(number_format, phone_candidate):
                return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_add_phone(user_command, number_format, name):
    if len(user_command) < 3:
        return "Give me name and new phone(s) please\n"
    if name[0].isdigit():
        return "A name cannot begin with a number!\n"
    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"
    for phone_candidate in user_command[2:]:
        if not re.search(number_format, phone_candidate):
            return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_change(user_command, number_format, name):
    if not contact_dictionary:
        return "No contact records available. You can add records\n"
    if len(user_command) < 4:
        return "Give me name and 2 phones please (current and new)\n"
    if name[0].isdigit():
        return "A name cannot begin with a number!\n"
    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"
    if not re.search(number_format, user_command[2]):
        return "The number(s) is invalid: contains invalid characters or incorrect length\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_phone(user_command, name):
    if not contact_dictionary:
        return "No contact records available\n"
    if len(user_command) < 2:
        return "Give me a name too, please\n"
    if name[0].isdigit():
        return "A name cannot begin with a number!\n"
    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"


def input_error(handler):
    '''User error handler
    incoming: handler (function)
    return: result(str) or exception_function(handler(user_command))'''
    # => user input command items in the list
    def exception_function(user_command):

        number_format = r'^\+[0-9)(-]{12,16}$'
        validation = None
        if len(user_command) > 1:
            name = user_command[1]

        if handler.__name__ == "handler_add":
            validation = validation_add(user_command, number_format, name)

        elif handler.__name__ == "handler_add_phone":
            validation = validation_add_phone(
                user_command, number_format, name)

        elif handler.__name__ == "handler_change":
            validation = validation_change(user_command, number_format, name)

        elif handler.__name__ == "handler_phone":
            validation = validation_phone(user_command, name)

        elif handler.__name__ == "handler_showall":
            if not contact_dictionary:
                return "No contact records available\n"

        if validation:
            return validation

        try:
            result = handler(user_command)

        except KeyError as error:
            return f"An incorrect name was entered ({error}), not found in the book"

        except ValueError as error:
            return f"I don't know such commands ({error})"

        except IndexError as error:
            return f"No values in database ({error})"

        except Exception as error:
            return f"Something went wrong ({error})"

        if result is None:
            return "No contact record available"

        return result

    return exception_function


@input_error
def handler_phone(user_command: list) -> str:
    '''"phone ...." With this command, the bot outputs the phone number for the specified 
    contact to the console. Instead of ... the user enters the name of the contact 
    whose number should be displayed.
    incoming: list of user command (name of user)
    return: phone number of user'''
    phones = ""
    name = user_command[1]
    for phone in (contact_dictionary[name]).phones:
        phones += f"{phone.value}; "
    return phones


@input_error
def handler_change(user_command: list) -> str:  # list of str
    '''"change ..." With this command, the bot stores the new phone number 
    of the existing contact in memory. Instead of ... the user enters 
    the name and phone numbers (current and new), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    current_phone = user_command[2]
    new_phone = user_command[3]
    contact_dictionary[name].change_phone(current_phone, new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)

    return "The record has been updated\n"


@input_error
def handler_add(user_command: list) -> str:
    '''"add ...". With this command, the bot saves 
    a new contact in memory (in the dictionary, for 
    example). Instead of ... the user enters the name 
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    new_record = Record(name)  # Record(Name(name))
    contact_dictionary.add_record(new_record)
    if len(user_command) > 2:
        phones = user_command[2:]
        for new_phone in phones:
            contact_dictionary[name].add_phone(new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record have been added\n"


@input_error
def handler_add_phone(user_command: list) -> str:
    '''"add ...". With this command, the bot saves 
    a new phones to contact in memory (in the dictionary, for 
    example). Instead of ... the user enters the name 
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    phones = user_command[2:]
    for new_phone in phones:
        contact_dictionary[name].add_phone(new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record have been added\n"


def handler_exit(_=None) -> str:
    return "Good bye!"


@input_error
def handler_showall(_=None) -> str:
    '''"show all". With this command, the bot outputs all saved 
    contacts with phone numbers to the console.
    incoming: not_matter: any
    return: string of all users'''

    all_list = "Entries in your contact book:"
    for name in contact_dictionary:
        all_list += f"\n{name} -> phone(s): "  # name.value
        for phone in contact_dictionary[name].phones:
            all_list += f"{phone.value}; "

    return all_list


def main_handler(user_command: list):
    '''All possible bot commands
    incoming: user command
    return: function according to the command'''
    all_command = {"hello": handler_hello,
                   "add": handler_add,
                   "addphone": handler_add_phone,
                   "change": handler_change,
                   "phone": handler_phone,
                   "showall": handler_showall,
                   "goodbye": handler_exit,
                   "close": handler_exit,
                   "exit": handler_exit}

    if all_command.get(user_command[0].lower(), "It is unclear") != "It is unclear":
        return all_command.get(user_command[0].lower())(user_command)
    return "It is unclear"


def handler_hello(_=None) -> str:
    return "How can I help you?\n"


def parser(user_input: str) -> list:
    '''Command parser. The part responsible for parsing 
    strings entered by the user, extracting keywords and 
    command modifiers from the string.
    incoming: string from user
    return: list of comands'''
    words = user_input.strip().split(" ")
    if len(words) >= 2 and words[0].lower() == "good" and words[1].lower() == "bye":
        words = ["goodbye"]
    if len(words) >= 2 and words[0].lower() == "show" and words[1].lower() == "all":
        words = ["showall"]
    if len(words) >= 2 and words[0].lower() == "add" and words[1].lower() == "phone":
        words = ["addphone"] + words[2:]
    words[0] = words[0].lower()
    return words


def main():
    """A new address book was generated at the beginning
    line 112: contact_dictionary = gen_AddressBook(16)
    """
    # global contact_dictionary
    # load contact dict if it available:
    # contact_dictionary = helper_opener()[0]

    while True:
        user_command = input()
        user_request = parser(user_command)
        bot_answer = main_handler(user_request)
        print(bot_answer)
        if bot_answer == "Good bye!":
            break

    exit()


if __name__ == "__main__":
    exit(main())
