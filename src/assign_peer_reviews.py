import pandas as pd
from helpers import auto_submit
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

        original_peer_reviews = settings.ASSIGNMENT_PR.get_peer_reviews()

        print(original_peer_reviews)



        _prompt_for_confirmation([("Do you need to autosubmit for: ", settings.ASSIGNMENT.name)])

        students = settings.COURSE.get_users(enrollment_type=['student'])
        auto_submit(students, settings.ASSIGNMENT)
    