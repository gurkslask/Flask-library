import unittest
import time
import os
from app.main.LibraryFunctions import Libraryfunctions


class Test(unittest.TestCase):
    """docstring for Test unittest.TestCase """
    def setUp(self):
        self.CheckOutText = """CheckedOut = True"""
        self.project = 'test_Projekt'
        self.project3 = 'test_Projekt3'
        self.projects_folder = 'test_Projects'
        self.uploads_folder = os.path.join(self.projects_folder, 'test_upload')
        if self.projects_folder not in os.listdir():
            os.mkdir(self.projects_folder)
        os.chdir(self.projects_folder)
        if self.project not in os.listdir():
            os.mkdir(self.project + '/')
        os.chdir('..')
        self.Lf = Libraryfunctions()
        self.Lf.ProjectFolderPath = os.path.join(
            os.getcwd(), self.projects_folder)
        self.Lf.StaticFolderPath = self.Lf.ProjectFolderPath
        self.Lf.UploadFolderPath = self.uploads_folder
        self.Lf.InitProject(self.project)

    def test_init(self):
        j = self.Lf.ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], False)

    def test_init_Project(self):
        self.Lf.InitProject(self.project3)
        j = self.Lf.ReadProjectDict(self.project3)
        self.assertEqual(j['CheckedOut'], False)

    def test_files(self):
        self.assertIn(self.projects_folder, os.listdir())

    def test_files2(self):
        self.assertIn(self.project, os.listdir(self.projects_folder))

    def test_CheckOut(self):
        self.Lf.CheckOut(self.project)
        j = self.Lf.ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], True)

    def test_CheckIn(self):
        self.Lf.CheckIn(self.project)
        j = self.Lf.ReadProjectDict(self.project)
        self.assertEqual(j['CheckedOut'], False)

    def test_zip(self):
        self.Lf.ZipPdearoject(self.project)
        self.assertGreater(
            os.path.getsize(
                '{}.zip'.format(
                    os.path.join(self.projects_folder, self.project))), 180)

    def test_unzip(self):
        self.Lf.UnZipProject(self.project)
        self.assertEqual(6, os.listdir(self.uploads_folder))

    def test_Delete(self):
        self.Lf.DeleteProject(self.project)
        time.sleep(1)
        self.assertFalse(self.project in os.listdir(self.projects_folder))

    def test_CheckInZip(self):
        #self.Lf.UnZipProject(self.project)
        pass


if __name__ == '__main__':
    unittest.main()
