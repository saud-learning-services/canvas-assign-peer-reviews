"""
This file is responsible for defining/initializing global variables.

authors:
@markoprodanovic, @alisonmyers
"""

import os


# Project ROOT directory
ROOT = os.path.dirname(os.path.abspath(__file__))

# Canvas object to provide access to Canvas API
COURSE = None

# Assignment object representing Canvas assignment specified by user input
ASSIGNMENT = None

PR_SOURCE = None

ASSIGNMENT_PR = None
GROUP_PR = None