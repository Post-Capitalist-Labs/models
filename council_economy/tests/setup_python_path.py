import sys
import os

# Construct the path to the 'council_economy.py' file
script_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(script_dir, '..', 'council_economy')
absolute_path = os.path.abspath(relative_path)

# Add the directory to sys.path
sys.path.append(absolute_path)
