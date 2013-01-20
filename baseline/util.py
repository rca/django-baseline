import re

from subprocess import PIPE, Popen

from django.utils import six

HEROKU_CONFIG_RE = re.compile(r'(?P<key>[^:]*):\s+(?P<value>.*)')


class HerokuError(Exception):
    pass

def convert_bool(value):
    """
    Returns the value as a boolean if appropriate

    The value is converted into a boolean if possible. The value will be
    returned unmodified if no suitable conversion found.
    """
    if value in ('yes', 'true', 'True'):
        value = True
    elif value in ('no', 'false', 'False'):
        value = False

    return value

def convert_int(value):
    """
    Return the value as an integer if it looks like a number. The value will be
    returned unmodified if no suitable conversion found.
    """
    try:
        return int(value)
    except ValueError:
        return value

def convert_sequence(value):
    if not isinstance(value, six.string_types):
        return value

    new_value = value
    first = value[0]
    last = value[-1]

    # check to see if the string uses parens or square brackets as leading
    # and trailing characters
    if first in ('(', '[') and last in (')', ']'):
        new_value = []
        for item in value[1:-1].split(','):
            item = item.strip()
            if item[0] in ('"', "'"):
                item = item[1:]
            if item[-1] in ('"', "'"):
                item = item[:-1]

            new_value.append(item)

    # if the leading character is a paren, convert to tuple
    if first == '(':
        new_value = tuple(new_value)

    return new_value

def get_heroku_config():
    heroku_config = {}
    command = ['heroku', 'config']

    try:
        heroku = Popen(command, stdout=PIPE)
    except OSError, exc:
        if exc[0] != 2:
            raise

        raise HerokuError('Heroku config failed: {0}'.format(exc), ' '.join(command))

    output = heroku.communicate()[0]
    for line in output.splitlines():
        matches = HEROKU_CONFIG_RE.match(line)
        if matches:
            heroku_config[matches.group('key')] = matches.group('value')

    return heroku_config

def set_heroku_config(**config):
    args = ['{0}={1!r}'.format(a, b) for a, b in config.items()]
    command = ['heroku', 'config:add'] + args

    try:
        heroku = Popen(command, stdout=PIPE, stderr=PIPE)
    except OSError, exc:
        if exc[0] != 2:
            raise

        raise HerokuError('Heroku config failed: {0}'.format(exc), ' '.join(command))

    stdout, stderr = heroku.communicate()
    status = heroku.wait()
    if status != 0:
        raise HerokuError('Heroku config failed: {0} (stdout: {1}, stderr: {2})'.format(' '.join(command), stdout, stderr), ' '.join(command))

def warn(message, color='yellow', name='Warning', prefix='', print_traceback=True):
    import sys
    from django.utils.termcolors import make_style

    red = make_style(fg=color, opts=('bold',))

    if print_traceback:
        import traceback
        traceback.print_exc()

    sys.stderr.write('{0}{1}: {2}\n'.format(prefix, red(name), message))
