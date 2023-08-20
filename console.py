#!/usr/bin/env python3
"""This module defines the command line interpreter for the HBNB project."""
import cmd
import models

# Dictionary to store available classes
classes = {
    "BaseModel": models.BaseModel,
    "User": models.User,
    "State": models.State,
    "City": models.City,
    "Amenity": models.Amenity,
    "Place": models.Place,
    "Review": models.Review
}

class HBNBCommand(cmd.Cmd):
    """Defines the command prompt class."""
    
    prompt = "(hbnb) "
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True
    
    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass
    
    def do_create(self, args):
        """Create a new instance of a class"""
        if not args:
            print("** class name missing **")
            return
    
        # Split the arguments into a list
        args_list = args.split()

        # The first argument is the class name
        class_name = args_list[0]

        # Check if the class exists in the dictionary of available classes
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        # Remove the class name from the list of arguments
        args_list.pop(0)

        # Initialize an empty dictionary to store the attributes
        attributes = {}

        # Iterate through the list of arguments to parse attributes
        for arg in args_list:
            # Split the argument into attribute name and value
            parts = arg.split('=')
            if len(parts) == 2:
                attr_name = parts[0]
                attr_value = parts[1]

                # Try to convert the attribute value to the appropriate type
                if attr_value.startswith('"') and attr_value.endswith('"'):
                    attributes[attr_name] = attr_value[1:-1]
                elif '.' in attr_value:
                    try:
                        attributes[attr_name] = float(attr_value)
                    except ValueError:
                        attributes[attr_name] = attr_value
                else:
                    try:
                        attributes[attr_name] = int(attr_value)
                    except ValueError:
                        attributes[attr_name] = attr_value

        # Create a new instance of the class with the parsed attributes
        new_instance = classes[class_name](**attributes)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance"""
        if not args:
            print("** class name missing **")
            return
        
        args_list = args.split()
        class_name = args_list[0]
        
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args_list[1]
        key = "{}.{}".format(class_name, instance_id)
        
        objects = models.storage.all()
        
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")
    
    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        if not args:
            print("** class name missing **")
            return
        
        args_list = args.split()
        class_name = args_list[0]
        
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args_list[1]
        key = "{}.{}".format(class_name, instance_id)
        
        objects = models.storage.all()
        
        if key in objects:
            del objects[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """Prints all string representation of all instances"""
        args_list = args.split()
        obj_list = []

        if args_list and args_list[0] in classes:
            class_name = args_list[0]
            objects = models.storage.all()
            for key, obj in objects.items():
                if class_name == key.split('.')[0]:
                    obj_list.append(str(obj))
        elif not args_list:
            objects = models.storage.all()
            for obj in objects.values():
                obj_list.append(str(obj))
        else:
            print("** class doesn't exist **")
            return

        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")
    
    def do_update(self, args):
        """Updates an instance based on the class name and id"""
        if not args:
            print("** class name missing **")
            return
        
        args_list = args.split()
        class_name = args_list[0]
        
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args_list[1]
        key = "{}.{}".format(class_name, instance_id)
        
        objects = models.storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return

        if len(args_list) < 4:
            print("** value missing **")
            return
        
        attr_name = args_list[2]
        attr_value = args_list[3]

        obj = objects[key]
        setattr(obj, attr_name, attr_value)
        models.storage.save()

    def default(self, line):
        """Called on an input line when the command prefix is not recognized."""
        args_list = line.split(".")
        
        if len(args_list) >= 2 and args_list[0] in classes and args_list[1] == "all()":
            self.do_all(args_list[0])
        elif len(args_list) >= 2 and args_list[0] in classes and args_list[1] == "count()":
            count = 0
            objects = models.storage.all()
            for key in objects.keys():
                if args_list[0] == key.split('.')[0]:
                    count += 1
            print(count)
        elif len(args_list) >= 3 and args_list[0] in classes and args_list[1] == "show()":
            instance_id = args_list[2][1:-2]
            self.do_show("{} {}".format(args_list[0], instance_id))
        elif len(args_list) >= 3 and args_list[0] in classes and args_list[1] == "destroy()":
            instance_id = args_list[2][1:-2]
            self.do_destroy("{} {}".format(args_list[0], instance_id))
    
    def help_quit(self):
        """Prints help information for the quit command"""
        print("Quit command to exit the program")
    
    def help_EOF(self):
        """Prints help information for the EOF command"""
        print("EOF command to exit the program")
    
    def help_create(self):
        """Prints help information for the create command"""
        print("Create a new instance of a class")
        print("Usage: create <class_name> [<attribute_name>=<attribute_value> ...]")
    
    def help_show(self):
        """Prints help information for the show command"""
        print("Prints the string representation of an instance")
        print("Usage: show <class_name> <instance_id>")
    
    def help_destroy(self):
        """Prints help information for the destroy command"""
        print("Deletes an instance based on the class name and id")
        print("Usage: destroy <class_name> <instance_id>")
    
    def help_all(self):
        """Prints help information for the all command"""
        print("Prints string representation of all instances")
        print("Usage: all [class_name]")
    
    def help_update(self):
        """Prints help information for the update command"""
        print("Updates an instance based on the class name and id")
        print("Usage: update <class_name> <instance_id> <attribute_name> <attribute_value>")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
