import unittest
import os
from LibraryFunctions import CheckOut, InitProject, ReadProjectDict, CheckIn


class Test(unittest.TestCase):
    """docstring for Test unittest.TestCase """
    def setUp(self):
        self.CheckOutText = """CheckedOut = True"""
        self.project = 'test_Projekt'
        self.value = 30
        if 'Projects' not in os.listdir():
            os.mkdir('Projects/')
        os.chdir('Projects')
        if self.project not in os.listdir():
            os.mkdir(self.project + '/')
        os.chdir('..')
        InitProject(self.project)

    def test_init(self):
        j = ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], False)

    def test_files(self):
        self.assertIn('Projects', os.listdir())

    def test_files2(self):
        self.assertIn(self.project, os.listdir('Projects'))

    def test_CheckOut(self):
        CheckOut(self.project)
        j = ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], True)

    def test_CheckIn(self):
        CheckIn(self.project)
        j = ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], False)



if __name__ == '__main__':
    unittest.main()
