import os
import sys

## Set root directory path for easier module import
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

## Disable creation of __pycache__ directories
sys.dont_write_bytecode = True