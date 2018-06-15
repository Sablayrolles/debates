from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

import os
for module in os.listdir(os.path.dirname(__file__)):
    if not isfile(module) and (module == '__init__.py' or module[-3:] != '.py' or module[0:2] == "__"):
        continue
    __import__(module[:-3], locals(), globals())
del module