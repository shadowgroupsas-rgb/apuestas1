import sys
import os

# Adds the current directory to the python path
sys.path.append(os.getcwd())

from app import app as application
