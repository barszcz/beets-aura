# This file is part of beets.
# Copyright 2013, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""A Web interface to beets."""
from beets.plugins import BeetsPlugin
from beetsplug.web import WebPlugin
from beets import ui
from .aura import configure_aura

# Utilities.
# Plugin hook.
class BeetsHook(WebPlugin):
    def __init__(self):
        super(WebPlugin, self).__init__()
        self.config.add({
            'host': u'',
            'port': 8337,
            'daemonize': False
        })
        self.app = 0

    def commands(self):
        cmd = ui.Subcommand('aura', help='start a REST API interface.')
        cmd.parser.add_option('-d', '--debug', action='store_true',
                              default=False, help='debug mode')

        # TODO: Implement daemonization, maybe?
        # Would be good for simple usage, but bad for production.
        #cmd.parser.add_option('-D', '--daemonize', action='store_true',
        #                      default=False, help='daemonize server')

        def func(lib, opts, args):
            args = ui.decargs(args)
            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))
            aura = configure_aura()
            aura.run(host=self.config['host'].get(unicode),
                    port=self.config['port'].get(int),
                    debug=opts.debug, threaded=True)
        cmd.func = func
        return [cmd]

class WSGIHook(object):
    '''Class for WSGI implementations to hook into'''
    def __init__(self):
        raise NotImplemented("WSGIHook Constructor Not Implemented")


