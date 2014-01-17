"""
Created on 09.12.2013

@author: udakak
"""

from ggs.core import Core

core = Core()
try:
    core.run()
except KeyboardInterrupt:
    print("stopping...")
    core.stop()
