'''
homework 10 test...
'''
from collections import UserDict
import random


def my_generator_names(quantity_limit: int) -> str:
    """
    Simplest generator Names (example: Name_0, Name_1, ...) in limited quantities
    incoming: quantity_limit (int)
    return: yield next name
    """
    counter = 0
    while counter < quantity_limit:
        yield f"Name_{counter}"
        counter += 1


def my_generator_phones(quantity_limit: int) -> str:
    """
    Simplest generator Phones (example: +38(063)0000000, +38(063)0000001,...) in limited quantities
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


'''
rec0 = Record(Name("Alf"))
rec1 = Record(Name("Den"), Phone("+380677777777"))
print(rec1.name.value)
print(rec1.phone[0].value)

rec2 = Record(Name("Ben"), Phone("+380677777778"), Phone("+380677777779"))
print(rec2.name.value)
print(rec2.phone[0].value)
print(rec2.phone[1].value)

rec3 = Record(Name("Ann"))
print(rec3.name.value)
print(rec3.phone)
rec3.add_phone("+380677777780")
print(rec3.phone[0].value)
rec3.add_phone("+380677777781")
print(rec3.phone[1].value)
rec3.add_phone("+380677777782")
print(rec3.phone[2].value)
rec3.change_phone("+380677777781", "+380677777783")
rec3.add_phone("+380677777781")
print(rec3.phone[1].value)
rec3.remove_phone("+380677777780")
print(rec3.phone[0].value)

book0 = AddressBook()
book0.add_record(rec0)
book0.add_record(rec1)
book0.add_record(rec2)
book0.add_record(rec3)
print(book0)
print(book0['Ann'])
print(book0['Ann'].name.value)
print(book0['Ann'].phone[1].value)
book0['Ann'].add_phone("+380677777784")
print(book0['Ann'].phone[3].value)
'''


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


my_first_address_book = gen_AddressBook(16)


def test_address_book(address_book):
    for record in address_book:
        print(record)
        for phone in address_book[record].phone:
            print(phone.value)


test_address_book(my_first_address_book)
