# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

if __name__ == '__main__':
    from nose import run
    run(argv=[sys.argv[0], '--all-modules'])
