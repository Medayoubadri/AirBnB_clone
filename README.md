
# AirBnB Clone - Command Interpreter

This is the first phase of the **AirBnB Clone** project. The goal of this phase is to implement a command-line interpreter that manages data for our AirBnB clone project. This console serves as the entry point to our application and is capable of:

- Creating new objects (e.g., users, places, etc.).
- Retrieving objects from storage.
- Performing operations like updating or deleting objects.
- Interfacing with a persistent file storage system.

---

## Description of the Command Interpreter

The command interpreter (console) is a shell-like tool used to interact with our application. It allows users to perform CRUD (Create, Read, Update, Delete) operations on objects, as well as other tasks, through textual commands.

---

### How to Start It

1. Clone this repository:

   ```bash
   git clone https://github.com/medayoubadri/AirBnB_clone.git
   cd AirBnB_clone
   ```

2. Start the console:

   ```bash
   ./console.py
   ```

---

### How to Use It

Once the console starts, you will see the `(hbnb)` prompt. From here, you can type commands to interact with the application.

#### Available Commands

- `help` - Displays help for available commands.
- `quit` - Exits the console.
- `EOF` - Exits the console (Ctrl+D).
- `create <class name>` - Creates a new instance of the specified class and prints its ID.
- `show <class name> <id>` - Displays an instance based on class name and ID.
- `destroy <class name> <id>` - Deletes an instance based on class name and ID.
- `all [<class name>]` - Displays all instances or all instances of a specific class.
- `update <class name> <id> <attribute name> <attribute value>` - Updates an instance with a new attribute.
- `<class name>.all()` - Retrieves all instances of a class.
- `<class name>.count()` - Counts the number of instances of a class.
- `<class name>.show("<id>")` - Displays an instance based on ID.
- `<class name>.destroy("<id>")` - Deletes an instance based on ID.
- `<class name>.update("<id>", <attribute name>, <attribute value>)` - Updates an instance.
- `<class name>.update("<id>", <dictionary>)` - Updates multiple attributes of an instance.

---

### Examples

1. **Create a new User:**

   ```bash
   (hbnb) create User
   1234-5678
   ```

2. **Show a User:**

   ```bash
   (hbnb) show User 1234-5678
   [User] (1234-5678) {<User details>}
   ```

3. **Update a User:**

   ```bash
   (hbnb) update User 1234-5678 name "John"
   ```

4. **Delete a User:**

   ```bash
   (hbnb) destroy User 1234-5678
   ```

5. **Count Instances:**

   ```bash
   (hbnb) User.count()
   2
   ```

6. **Display All Instances:**

   ```bash
   (hbnb) all
   [[User] (1234-5678) {<User details>}, ...]
   ```
