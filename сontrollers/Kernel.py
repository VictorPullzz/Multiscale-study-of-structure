##
# Class start all
##
from FileController import FileController

class Kernel():

    def __init__(self):
        createFile = FileController()
        createFile.getFile()

createFile = Kernel()
