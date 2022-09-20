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
import os
import pickle
import random


def my_generator_names(quantity_limit: int) -> str:
    """Simplest generator Names (example: Name_0, Name_1, ...) in limited quantities
    incoming: quantity_limit (int)
    return: yield next name
    """
    counter = 0
    while counter < quantity_limit:
        yield f"Name_{counter}"
        counter += 1


def my_generator_phones(quantity_limit: int) -> str:
    """Simplest generator Phones (example: +38(063)0000000, +38(063)0000001,...) in limited quantities
    incoming: quantity_limit (int)
    return: yield next phone
    """
    counter = 0
    while counter < quantity_limit:
        yield "+38(063){:07}".format(counter)
        counter += 1


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, Record):
        self.data.update({Record.name.value: Record})


class Field:  # super for all fields ... for the future?
    pass


class Name(Field):
    def __init__(self, value):
        # super().__init__(name) ... for the future?
        self.value = value


class Phone(Field):
    def __init__(self, value=None):  # *phone
        # super().__init__(phone) ... for the future?
        self.value = value


class Record(Name, Phone):  # add remove change  field

    def __init__(self, Name, *Phone):
        self.name = Name
        self.phone = list(Phone)

    def add_phone(self, phone_new):
        self.phone.append(Phone(phone_new))

    def remove_phone(self, phone_to_remove):
        for current_phone in self.phone:
            if current_phone.value == phone_to_remove:
                self.phone.remove(current_phone)
                break

    def change_phone(self, phone_to_change, phone_new):
        for current_phone in self.phone:
            if current_phone.value == phone_to_change:
                self.phone.insert(self.phone.index(
                    current_phone), Phone(phone_new))
                self.phone.remove(current_phone)
                break


def gen_AddressBook(max_names: int) -> AddressBook:
    """Simplest generator simplest AddressBook
    incoming: max_names is quantity limit (int)
    return: book0 - instance of the filled class AddressBook
    """
    book0 = AddressBook()
    counter = 0
    name = my_generator_names(max_names)
    phone = my_generator_phones(max_names * 3)
    while counter < max_names:
        rec0 = Record(Name(next(name)))
        phones_quantity = random.choice([1, 2, 3, ])

        while phones_quantity:
            rec0.add_phone(next(phone))
            phones_quantity -= 1

        book0.add_record(rec0)
        counter += 1

    return book0


# contact_dictionary = AddressBook()
# Next - only for tests... :
contact_dictionary = gen_AddressBook(16)  # ! =AddressBook()


def input_error(handler):
    '''User error handler
    incoming: handler (function)
    return: result(str) or exception_function(handler(user_command))'''
    # => user input command items in the list
    def exception_function(user_command):

        number_separators = "+()-0123456789"

        if handler.__name__ == "h_add":
            if len(user_command) < 2:
                return "Give me name OR name and phone please\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"
            if len(user_command) >= 4:
                for phone_candidate in user_command[4:]:
                    if len([i for i in phone_candidate if i in number_separators]) != len(phone_candidate):
                        return "The number(s) contains invalid characters\n"

        elif handler.__name__ == "h_add_phone":
            if len(user_command) < 3:
                return "Give me name and new phone(s) please\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"
            if len([i for i in user_command[2] if i in number_separators]) != len(user_command[2]):
                return "The number contains invalid characters\n"

        elif handler.__name__ == "h_change":
            if not contact_dictionary:
                return "No contact records available. You can add records\n"
            if len(user_command) < 4:
                return "Give me name and 2 phones please (current and new)\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"
            if len([i for i in user_command[2] if i in number_separators]) != len(user_command[2]):
                return "The number contains invalid characters\n"

        elif handler.__name__ == "h_phone":
            if not contact_dictionary:
                return "No contact records available\n"
            if len(user_command) < 2:
                return "Give me a name too, please\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"

        elif handler.__name__ == "h_showall":
            if not contact_dictionary:
                return "No contact records available\n"

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


def helper_try_open_file(path_file: str) -> str:
    '''Checks if the database file exists and checks if the filename is free if not
    incoming: path_file is name of file
    return: name of file'''
    stored_dict = {}
    if os.path.isdir(path_file):
        while os.path.exists(path_file):
            path_file = "new_one_" + path_file

    if not os.path.isfile(path_file):
        with open(path_file, "ab") as words_file:
            pickle.dump(stored_dict, words_file)

    return path_file


@input_error
def h_phone(user_command: list) -> str:
    '''"phone ...." With this command, the bot outputs the phone number for the specified 
    contact to the console. Instead of ... the user enters the name of the contact 
    whose number should be displayed.
    incoming: list of user command (name of user)
    return: phone number of user'''
    phones = ""
    for phone in contact_dictionary[user_command[1]].phone:
        phones += f"{phone.value}; "
    return phones


@input_error
def h_change(user_command: list) -> str:  # list of str
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
def h_add(user_command: list) -> str:
    '''"add ...". With this command, the bot saves 
    a new contact in memory (in the dictionary, for 
    example). Instead of ... the user enters the name 
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    new_record = Record(Name(name))
    contact_dictionary.add_record(new_record)
    if len(user_command) > 2:
        for new_phone in user_command[2:]:
            contact_dictionary[name].add_phone(new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record have been added\n"


@input_error
def h_add_phone(user_command: list) -> str:
    '''"add ...". With this command, the bot saves 
    a new phones to contact in memory (in the dictionary, for 
    example). Instead of ... the user enters the name 
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    for new_phone in user_command[2:]:
        contact_dictionary[name].add_phone(new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record have been added\n"


def h_exit(_=None) -> str:
    return "Good bye!"


@input_error
def h_showall(_=None) -> str:
    '''"show all". With this command, the bot outputs all saved 
    contacts with phone numbers to the console.
    incoming: not_matter: any
    return: string of all users'''

    all_list = "Entries in your contact book:"
    for record in contact_dictionary:
        all_list += f"\n{record} -> phone(s): "
        for phone in contact_dictionary[record].phone:
            all_list += f"{phone.value}; "

    return all_list


def helper_opener() -> tuple:
    '''loads a list of users from a file
    incoming: None
    return: list of user dictionary and new path file(database)'''
    path_file = "ABook.bdata"
    new_path_file = helper_try_open_file(path_file)

    with open(new_path_file, "rb") as f:
        stored_dict = pickle.load(f)

    return (stored_dict, new_path_file)


def main_handler(user_command: list):
    '''All possible bot commands
    incoming: user command
    return: function according to the command'''
    all_command = {"hello": h_hello,
                   "add": h_add,
                   "addphone": h_add_phone,
                   "change": h_change,
                   "phone": h_phone,
                   "showall": h_showall,
                   "goodbye": h_exit,
                   "close": h_exit,
                   "exit": h_exit}

    if all_command.get(user_command[0].lower(), "It is unclear") != "It is unclear":
        return all_command.get(user_command[0].lower())(user_command)
    return "It is unclear"


def h_hello(_=None) -> str:
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
