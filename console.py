#!/usr/bin/python3
import cmd

class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB."""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Exit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Handle end of file (EOF) to exit the program."""
        print("")  # Print newline to avoid weird terminal behavior
        return True

    def emptyline(self):
        """Override default behavior to do nothing on empty input."""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
