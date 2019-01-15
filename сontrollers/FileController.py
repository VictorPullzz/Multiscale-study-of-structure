import os
import sys
import shutil

# import cutom class
from FdmnesController import FdmnesController

##
# Сlass for work file XYZ
##
class FileController:
    # conts path calculations
    PATH_CALCULATE = "../calculations/"

    # const path clusters
    PATH_CLUSTERS = "../data/clusters/"

    # const path fdmnes template
    PATH_TEMPLATE_FDMNES = "../templates/fdmnes/"

    # const path name file fdmnes
    NAME_TEMPLATE_FDMNES = "Pt_inp_tpl"

    # const path name file fdmnes
    NAME_FILE_FDMNES = "Pt_inp"

    # const path name file fdmnes
    FORMAT_FDMNES = ".txt"

    # method for get data from file
    def getFile(self):
        for fileName in os.listdir(self.PATH_CLUSTERS):

            # read file
            with open(self.PATH_CLUSTERS + "/" + fileName, "r") as file:
                strFilePosition = ''

                for fileLine in file:
                    if 'Pt' in fileLine:
                        strFilePosition += fileLine

                self.includeIntemplate(strFilePosition, fileName)

            file.close()

            sys.exit();

    # method for write and save new file
    def includeIntemplate(self, strPosition, fileName):
        # create path with template fdmnes
        path = self.PATH_TEMPLATE_FDMNES + self.NAME_TEMPLATE_FDMNES + self.FORMAT_FDMNES

        with open(path, 'r') as file:
            oldData = file.read()

        # replase unnecessary data
        strPosition = strPosition.replace('78', '')
        strPosition = strPosition.replace('Pt', '78')

        # clear file name
        newFileName = fileName.replace('.xyz', '')

        # convert data in need format
        newDate = oldData.replace('{{ coordinate }}', strPosition)

        # folder with calculations
        directory = self.PATH_CALCULATE + newFileName

        # create folder for fdmnes calculations
        newPath = self.createFolderFdmnes(directory)

        fdmnes = FdmnesController(directory)
        fdmnes.run()

        with open(newPath, 'w') as file:
            file.write(newDate)
            print('Файл успешно сохранен в директорию')

    # method for create folder
    def createFolderFdmnes(self, directory):
        # define the access rights
        access_rights = 0o755

        # check if exist directory
        if not os.path.exists(directory):
            try:
                os.mkdir(directory, access_rights)
            except OSError:
                print("Создать директорию %s не удалось" % directory)
            else:
                print("Успешно создана директория %s" % directory)
        else:
            print("Директория уже существует %s" % directory)

        self.cloneFdmnesFile(directory)

        return directory + '/' + self.NAME_FILE_FDMNES + self.FORMAT_FDMNES

    def cloneFdmnesFile(self, directory):
        files = [
            'fdmfile.txt',
            'spacegroup.txt',
            'xsect.dat'
        ]

        try:
            for f in files:
                shutil.copy2(self.PATH_TEMPLATE_FDMNES + f, directory)
        except OSError:
            print("Не удалось клонировать файлы в %s" % directory)
        else:
            print("Были временно отклонированы файлы в директорию %s" % directory)
