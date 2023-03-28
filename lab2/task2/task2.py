import re
import json

class UserContainer:
    def __init__(self, username):
        self.username = username
        self.container = set()

    def add(self, *keys):
        for key in keys:
            if key not in self.container:
                self.container.add(key)
                print(f"Added {key} to {self.username}'s container")
            else:
                print(f"{key} already exists in {self.username}'s container")

    def remove(self, key):
        if key in self.container:
            self.container.remove(key)
            print(f"Removed {key} from {self.username}'s container")
        else:
            print(f"{key} does not exist in {self.username}'s container")

    def find(self, *keys):
        found = False
        for key in keys:
            if key in self.container:
                print(f"{key} exists in {self.username}'s container")
                found = True
        if not found:
            print(f"No such elements in {self.username}'s container")

    def show(self):
        print(f"{self.username}'s container: {', '.join(self.container)}")

    def grep(self, regex):
        found = False
        for key in self.container:
            if re.search(regex, key):
                print(f"Found {key} in {self.username}'s container")
                found = True
        if not found:
            print(f"No such elements in {self.username}'s container")

    def save(self):
        with open(f"{self.username}.json", "w") as f:
            json.dump(list(self.container), f)
        print(f"{self.username}'s container saved")

    def load(self):
        try:
            with open(f"{self.username}.json", "r") as f:
                data = json.load(f)
            self.container = set(data)
            print(f"{self.username}'s container loaded")
        except FileNotFoundError:
            print(f"No saved container for {self.username}")


class UserStorage:

    def __init__(self):
        self.users = {}

    def switch_user(self, username):

        if username not in self.users:
            self.users[username] = UserContainer(username)
        return self.users[username]

    def save_all(self):
        for user_container in self.users.values():
            user_container.save()

    def load_all(self):
        for user_container in self.users.values():
            user_container.load()


def main():
    storage = UserStorage()
    while True:
        username = input("Enter username: ")
        user_container = storage.switch_user(username)

        while True:
            command = input("Enter command: ")
            if command == "add":
                keys = input("Enter keys separated by space: ").split()
                user_container.add(*keys)
            elif command == "remove":
                key = input("Enter key to remove: ")
                user_container.remove(key)
            elif command == "find":
                keys = input("Enter keys separated by space: ").split()
                user_container.find(*keys)
            elif command == "show":
                user_container.show()
            elif command == "grep":
                regex = input("Enter regular expression: ")
                user_container.grep(regex)
            elif command == "save":
                user_container.save()
            elif command == "load":
                user_container.load()
            elif command == "switch":
                break
            elif command == "exit":
                storage.save_all()
                print("Exiting...")
                return
            else:
                print("Invalid command, try again")



main()