#!/usr/bin/python3
""" Module with Unittest for the HBNBCommand class.
    """
import inspect
import os
import pycodestyle
import unittest
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand(unittest.TestCase):
    """ Testing the HBNBCommand class of the program.
        """

    def test_module_documentation(self):
        """ Test if HBNBCommand module is documented.
            """
        self.assertTrue(HBNBCommand.__doc__)

    def test_class_documentation(self):
        """ Test if HBNBCommand class is documented.
            """
        self.assertTrue(HBNBCommand.__doc__)

    def test_methods_documentation(self):
        """ Test if all HBNBCommand methods are documented.
            """
        methods = inspect.getmembers(HBNBCommand)
        for method in methods:
            self.assertTrue(inspect.getdoc(method))

    def test_pycodeStyle(self):
        """Test that we conform to PEP-8.
            """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (pycodestyle).")

    def test_prompt(self):
        """ Test the prompt
            """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """ Check the case of empty line
            """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue().strip())

    def test_UnknowCommand(self):
        """ Test an unknow command
            """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("fdfdf")
            self.assertEqual("*** Unknown syntax: fdfdf", f.getvalue().strip())
