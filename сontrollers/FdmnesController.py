##
# Class work with FDMNES
##
import subprocess

class FdmnesController:

    # path where store fdmnes files
    FDMNES_PATH = ''

    def __init__(self, pathToFdmnes):
        self.FDMNES_PATH = pathToFdmnes

    def run(self):
        try:
            subprocess.check_output('cd ' + self.FDMNES_PATH, shell=True)
        except subprocess.CalledProcessError as e:
            print('Команда \n> {}\nзавершилась с кодом {}'.format(e.cmd, e.returncode))
