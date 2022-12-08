"""
authors:
@markoprodanovic, @alisonmyers
"""

import settings
import pandas as pd
from util import shut_down
from canvasapi import Canvas
from termcolor import cprint, colored
import os
from dotenv import load_dotenv
load_dotenv() 

URL = os.getenv('API_URL')
KEY = os.getenv('API_TOKEN')

def _get_groups(course):
    groups = course.get_group_categories()
    groups_list = [i.__dict__ for i in groups]
    groups_df = pd.DataFrame(groups_list)[["id", "name"]]
    
    return(groups_df, groups_list)

def get_user_inputs(URL, KEY):
    """Prompt user for required inputs. Queries Canvas API throughout to check for
    access and validity errors. Errors stop execution and print to screen.

    Returns:
        Dictionary containing inputs
    """

    # prompt user for url and token
    url = URL
    token = KEY

    # Canvas object to provide access to Canvas API
    canvas = Canvas(url, token)

    # get user object
    try:
        user = canvas.get_user("self")
        cprint(f"\nHello, {user.name}!", "magenta")
        # shut_down('TEMP KILL SWITCH')
    except Exception as e:
        shut_down(
            """
            ERROR: could not get user from server.
            Please ensure token is correct and valid and ensure using the correct instance url.
            """
        )

    # get course object
    try:
        course_number = input(colored("Course Number: ", "blue"))
        course = canvas.get_course(course_number)
        cprint(f"{course.name}", "magenta")
    except Exception as e:
        shut_down("ERROR: Course not found. Please check course number.")

    # get how to Canvas Nesting Doll Peer Reviews
    try:
        # NOT IMPLEMENTED - NO PICK
        #title = "Please select how you to get student information for assigning peer reviews"
        #options = ["group", "assignment"]
        #peer_reviews_from = pick(options, title, multiselect=False, min_selection_count=1)

        
        settings.PR_SOURCE = "assignment"

        #if groups then
        #if peer_reviews_from[1] == 0:
        if False:
            try:
                title = "Please select which Canvas Group Set to use"
                groups_df, groups_list = _get_groups(course)
                print(groups_df)
                
                canvas_group_category_id = input("Please enter the Canvas group category id: ")
                #settings.PR_COURSE = "group"
                #canvas_group_category = _return_single_dict_match(groups_list, "id", canvas_group_category_id)
                #_prompt_for_confirmation([("Canvas Group Selected",  canvas_group_category)])
                #settings.GROUP_PR = canvas_group_category
                #peer_review_source = settings.GROUP_PR 
                #print(settings.GROUP_PR)
                shut_down("Doesn't work yet. Whoops")

            except Exception as e:
                shut_down(f"ERROR accessing Canvas groups. {e}")
            
        else:

            try:
                assignment_id_peerreviews = input(colored("Please enter the assignment id to access original peer reviews for: ", "blue"))
                assignment_peerreview = course.get_assignment(assignment_id_peerreviews)
                cprint(f"{assignment_peerreview.name}", "yellow")
                settings.ASSIGNMENT_PR = assignment_peerreview

            except:
                shut_down("ERROR: error getting original peer review info.")
    except:

        shut_down("ERROR: need to enter how you will get data for peer reviews")

    # get assignment object
    try:
        assignment_number = input(colored("Please enter the assignment id to create new peer reviews for: ", "blue"))
        assignment = course.get_assignment(assignment_number, include=["submissions"])
        cprint(f"{assignment.name}", "green")

    except Exception as e:
        shut_down("ERROR: Assignment not found. Please check assignment number.")

    # prompt user for confirmation


    # set course and assignment objects to global variables
    settings.COURSE = course
    settings.ASSIGNMENT = assignment
    settings.STUDENTS = course.get_users(enrollment_type=["student"])

    # return inputs dictionary
    return

def _prompt_for_confirmation(confirmationList=[], *args):
    """Prints user inputs to screen and asks user to confirm. Shuts down if user inputs
    anything other than 'Y' or 'y'. Returns otherwise.

    Args:
        a list of tuples: [(input_string, value)]
    Returns:
        None -- returns only if user confirms

    """
    cprint("\nConfirmation:", "blue")

    for i in confirmationList:
        cprint(f"{i[0]}: {i[1]}", "blue")
    print("\n")

    confirm = input(colored("Would you like to continue using the above information?[y/n]: ", "blue"))

    print("\n")

    if confirm == "y" or confirm == "Y":
        return
    elif confirm == "n" or confirm == "N":
        shut_down("Exiting...")
    else:
        shut_down("ERROR: Only accepted values are y and n")
