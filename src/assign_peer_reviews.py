from helpers import create_instance
from interface import get_user_inputs, _prompt_for_confirmation
import os
from dotenv import load_dotenv
import settings
load_dotenv() 

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

if __name__ == "__main__":
    get_user_inputs(API_URL, API_KEY)

    print(settings.PR_SOURCE)
    print(settings.ASSIGNMENT, settings.ASSIGNMENT_PR)

    if settings.PR_SOURCE == "assignment":
        _prompt_for_confirmation([("Selected course:", settings.COURSE.name), 
        ("You have selected to use peer reviews from ", settings.ASSIGNMENT_PR.name), ("to create new peer reviews in", settings.ASSIGNMENT.name)])

    #TODO - what if PR_SOURCE = group? (not implemented)

    