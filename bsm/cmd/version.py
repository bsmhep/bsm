import os
import click

from bsm import BSM_VERSION

class Version(object):
    def execute(self):
        click.echo('bsm {0}'.format(BSM_VERSION))