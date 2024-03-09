from collections import UserDict
from datetime import datetime
from collections import defaultdict
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Give me name and phone please."
            except KeyError:
                return "Enter the correct user name."
            except IndexError:
                return "Index out of range. Please provide valid input."
        return inner

    @input_error
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    @input_error
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    @input_error
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    @input_error
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    @input_error
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    @input_error
    def get_birthdays_per_week(self, name):
        today = datetime.today().date()
        birthdays_per_week = defaultdict(list)
        for record in self.data.values():
            if record.birthday is not None:
                birthday_date = datetime.strptime(
                    record.birthday.value, '%d.%m.%Y').date()
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_next_year = birthday_date.replace(
                        year=today.year+1)
                delta_days = (birthday_this_year - today).days
                if delta_days < 7:
                    birthday_weekday = birthday_this_year.strftime('%A')
                    if birthday_weekday == 'Sunday' or birthday_weekday == 'Saturday':
                        birthday_weekday = 'Monday'
                        birthdays_per_week[birthday_weekday].append(name)
                    else:
                        birthdays_per_week[birthday_weekday].append(name)

        birthday_next_week = sorted(birthdays_per_week.items())
        for i in birthday_next_week:
            print(i[0], ':', ', '.join(i[1]))

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.load()

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Give me name and phone please."
            except KeyError:
                return "Enter the correct user name."
            except IndexError:
                return "Index out of range. Please provide valid input."
        return inner

    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
        self.save()

    @input_error
    def find(self, name):
        if name in self.data:
            return self.data.get(name)

    @input_error
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        self.save()

    @input_error
    def add_birthday_for_contact(self, name, birthday):
        self.data[name.capitalize()].add_birthday(birthday)
        self.save()

    @input_error
    def show_birthday(self, name):
        if name.capitalize() in self.data:
            record = self.data[name.capitalize()]
            if record.birthday:
                return f"Contact name: {record.name.value}, birthday: {record.birthday.value}"
            else:
                return f"Contact {name.capitalize()} doesn't have a birthday specified."
        else:
            return f"Contact {name.capitalize()} doesn't exist in the address book."

    @input_error
    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays_per_week = defaultdict(list)
        for record in self.data.values():
            if record.birthday is not None:
                birthday_date = datetime.strptime(
                    record.birthday.value, '%d.%m.%Y').date()
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_next_year = birthday_date.replace(
                        year=today.year+1)
                delta_days = (birthday_this_year - today).days
                if delta_days < 7:
                    birthday_weekday = birthday_this_year.strftime('%A')
                    if birthday_weekday == 'Sunday' or birthday_weekday == 'Saturday':
                        birthday_weekday = 'Monday'
                        birthdays_per_week[birthday_weekday].append(record.name.value)
                    else:
                        birthdays_per_week[birthday_weekday].append(record.name.value)

        birthday_next_week = sorted(birthdays_per_week.items())
        for i in birthday_next_week:
            print(i[0], ':', ', '.join(i[1]))


def main():
    filename = r"C:\Users\samat\.vscode\python\GoIT(Core)\address_book.pkl"
    book = AddressBook(filename)
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = Record.parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            name, phone = args
            if not phone.isdigit() or len(phone) != 10:
                raise ValueError("Phone number must consist of 10 digits")
            if name.capitalize() in book.data:
                print(f"Contact {name.capitalize()} already exists in the address book.")
            else:
                record = Record(name.capitalize())
                record.add_phone(phone)
                book.add_record(record)
                print(f"Contact {name.capitalize()} has been adde in the address book.")
        elif command == "change":
            name, old_phone, new_phone = args
            if name.capitalize() in book.data:
                record = book.data[name.capitalize()]
                record.edit_phone(old_phone, new_phone)
                book.add_record(record)
                print(f"Phone number for {
                      name.capitalize()} has been changed.")
            else:
                print(f"Contact {name.capitalize()} doesn't exist in the address book.")
        elif command == "delete":
            name = args[0]
            if name.capitalize() in book.data:
                book.delete(name.capitalize())
                print(f"{name.capitalize()} has been deleted from the address book.")
            else:
                print(f"Contact {name.capitalize()} doesn't exist in the address book.")
        elif command == "phone":
            name = args[0]
            if name.capitalize() in book.data:
                print(book.find(name.capitalize()))
            else:
                print(f"Contact {name.capitalize()} doesn't in the address book.")
        elif command == "all":
            if book.data:
                print("All contacts:")
                for record in book.data.values():
                    print(record)
            else:
                print("Address book is empty.")
        elif command == "add_birthday":
            name, birthday = args
            try:
                datetime.strptime(birthday, '%d.%m.%Y')
            except ValueError:
                raise ValueError("Invalid date format. Please use DD.MM.YYYY format.")
            if name.capitalize() in book.data:
                book.add_birthday_for_contact(name, birthday)
                print(f"Birthday for {name.capitalize()} added.")
            else:
                print(f"Contact {name.capitalize()} doesn't exist in the address book.")
        elif command == "show_birthday":
            name = args[0]
            print(book.show_birthday(name))
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
