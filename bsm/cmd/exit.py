import click

from bsm.env import Env

class Exit(object):
    def execute(self, shell):
        shell.clear_script()

        env = Env()
        env.clean()
        set_env, unset = env.env_change()

        for e in unset:
            shell.unset_env(e)
        for k, v in set_env.items():
            shell.set_env(k, v)

        shell.undefine_bsm()

        click.echo(shell.script, nl=False)