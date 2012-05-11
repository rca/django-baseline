from subprocess import PIPE, Popen

def get_heroku_config():
    heroku_config = {}

    heroku = Popen(['heroku', 'config'], stdout=PIPE)
    output = heroku.communicate()[0]
    for line in output.splitlines():
        k, v = line.strip().split('=>', 1)
        heroku_config[k.strip()] = v.strip()

    return heroku_config

def set_heroku_config(**config):
    args = ['{0}={1}'.format(a, b) for a, b in config.items()]

    heroku = Popen(['heroku', 'config:add'] + args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = heroku.communicate()
    status = heroku.wait()
    if status != 0:
        raise Exception('Heroku config failed (stdout: {0}, stderr: {1})'.format(stdout, stderr))

def warn(message, color='yellow', name='Warning', prefix='', print_traceback=True):
    import sys
    from django.utils.termcolors import make_style

    red = make_style(fg=color, opts=('bold',))

    if print_traceback:
        import traceback
        traceback.print_exc()

    sys.stderr.write('{0}{1}: {2}\n'.format(prefix, red(name), message))
