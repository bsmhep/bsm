from bsm.cmd import Base
from bsm.cmd import CmdResult
from bsm.shell import Shell

class Init(Base):
    def execute(self, no_default, show_script, shell):
        output = ''
        if show_script and shell:
            cmd_name = self._bsm.config('app')['cmd_name']
            app_root = self._bsm.config('app').get('app_root', '')

            shell = Shell(shell, cmd_name, app_root)
            shell.add_script('init')
            output = shell.script

        if not no_default and 'version' in self._bsm.config('scenario'):
            self._bsm.load_release()
            self._bsm.load_release_package()

        return CmdResult(output=output, script_types='init')
