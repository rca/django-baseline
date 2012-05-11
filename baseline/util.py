def warn(message, color='yellow', name='Warning', prefix='', print_traceback=True):
    import sys
    from django.utils.termcolors import make_style

    red = make_style(fg=color, opts=('bold',))

    if print_traceback:
        import traceback
        traceback.print_exc()

    sys.stderr.write('{0}{1}: {2}\n'.format(prefix, red(name), message))
