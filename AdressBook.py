'''
homework 10 test...
'''
from collections import UserDict


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, Record):
        self.data.update({Record.name.value: Record})


class Field:  # super for all fields
    pass


class Name(Field):
    def __init__(self, value):
        # super().__init__(name)
        self.value = value


class Phone(Field):
    def __init__(self, value=None):  # *phone
        # super().__init__(phone)
        self.value = value


class Record(Name, Phone):  # add remove change  field

    def __init__(self, Name, *Phone):  # *phone
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
