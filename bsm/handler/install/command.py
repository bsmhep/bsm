from bsm.util import call_and_log


def run(param):
    format_dict = {}
    format_dict.update(param['package_path'])
    format_dict.update(param['prop'].get('path', {}))

    cwd = param['action_param'].get('cwd', '{main_dir}').format(**format_dict)

    cmds = param['action_param']['cmd']
    if not isinstance(cmds[0], list):
        cmds = [cmds]

    env = param.get('env')
    env_cmd = env.copy()
    for k, v in param['action_param'].get('env', {}).items():
        env_cmd[k] = v.format(**format_dict)

    ret = 0
    with open(param['log_file'], 'w') as f:
        for cmd in cmds:
            ret = call_and_log(cmd, log=f, cwd=cwd, env=env)
            if ret != 0:
                return {
                    'success': False,
                    'message': 'Command "{0}" failed with exit code: {1}'.format(cmd, ret),
                }

    return {'success': ret == 0, 'message': 'Command exit code: {0}'.format(ret)}
