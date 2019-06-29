import sys
import os

from bsm.shell.base import Base

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CSH_INIT = os.path.join(CUR_DIR, 'bsm.csh')


def _convert_csh_string(s):
    res = '\''
    for i in s:
        if i == '!':
            res += '\\!'
        elif i == '\n':
            res += '\\n'
        # "'" will be converted into four chars "'\''"
        elif i == '\'':
            res += '\'\\\'\''
        else:
            res += i
    res += '\''
    return res


class Csh(Base):
    def comment(self, content):
        ''' csh does not support comment when interactive
        '''
        return '\n'

    def print(self, content):
        lines = content.split('\n')
        newlines = ['echo ' + _convert_csh_string(l) for l in lines]
        return ';\n'.join(newlines) + ';\n'

    def print_env(self, env_name):
        return 'sh -c \'echo "${0}"\';\n'.format(env_name)

    def set_env(self, env_name, env_value):
        return 'setenv {0} {1};\n'.format(env_name, _convert_csh_string(env_value))

    def unset_env(self, env_name):
        return 'unsetenv {0};\n'.format(env_name)

    def alias(self, alias_name, alias_value):
        return 'alias {0} {1};\n'.format(alias_name, _convert_csh_string(alias_value))

    def unalias(self, alias_name):
        return 'unalias {0};\n'.format(alias_name)

    def source(self, script_path):
        return 'source \'{0}\';\n'.format(script_path)

    def script_init(self):
        python_exe = sys.executable or 'python'

        bsm_alias = '''\
alias {cmd_name} '\
set _bsm_python_exe="{python_exe}"; \
set _bsm_argv="\!*"; \
set _bsm_cmd_name="{cmd_name}"; \
set _bsm_app_root="{app_root}"; \
source "{csh_init}"; \
unset _bsm_app_root; \
unset _bsm_cmd_name; \
unset _bsm_argv; \
unset _bsm_python_exe; \
eval "exit $_bsm_exit"\
';
'''.format(cmd_name=self._cmd_name, python_exe=python_exe, app_root=self._app_root, csh_init=CSH_INIT)

        return bsm_alias

    def script_exit(self):
        bsm_exit = '''\
unalias {cmd_name};
'''.format(cmd_name=self._cmd_name)
        return bsm_exit
