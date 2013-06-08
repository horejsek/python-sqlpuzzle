# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

from nose import run
run(argv=[sys.argv[0], '--include', '.*test(\.py)?'])
