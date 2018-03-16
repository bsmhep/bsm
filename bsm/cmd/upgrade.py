import click

from pip import main

class Upgrade(object):
    def execute(self):
        def pip_install(package):
            main(['install', '--upgrade', package])

        pip_install('pip')
        pip_install('bsm')
