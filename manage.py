#!/usr/bin/env python

from __future__ import absolute_import

import sys
import unittest
from aura import configure_aura

def serve(args):
    aura = configure_aura()
    aura.run(threaded=True)

def test(args):
    unittest.main(module='test')

#if __name__ == '__main__':
cmd = sys.argv[1]
args = sys.argv[2:] if len(sys.argv) > 2 else []

locals()[cmd](args)
