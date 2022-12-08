import pandas as pd
from helpers import auto_submit
from interface import get_user_inputs, _prompt_for_confirmation
import os
from termcolor import colored, cprint
from dotenv import load_dotenv
import settings
load_dotenv() 

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def main():
    
    # get the user inputs
    # this creates necessary settings variables
    get_user_inputs(API_URL, API_KEY)
    
    COURSE = settings.COURSE
    ASSIGNMENT = settings.ASSIGNMENT
    PR_SOURCE = settings.PR_SOURCE
    ASSIGNMENT_PR = settings.ASSIGNMENT_PR
    STUDENTS = settings.STUDENTS
    
    #TODO - implement the group option
    GROUP_PR = settings.GROUP_PR 

    # get the students in the course as a dictionary (for reference to name)
    students_dict = _create_student_dict(STUDENTS)
    
    # get the peer reviews from the original assignment
    og_peer_reviews = _get_peer_reviews(ASSIGNMENT_PR)
    print(f"{colored(ASSIGNMENT_PR.name, 'yellow')} peer reviews:")
    print(og_peer_reviews)

    # for each user, get the list of who they were assessed by
    # in the new peer reviews, the user will assess the original assessees
    _check_for_auto_submit(ASSIGNMENT, STUDENTS)
    # for the new assignment, delete any existing peer reviews
    #TODO - add confirmation step here 
    # returns submissions, needed to assign new peer reviews


    _prompt_for_confirmation([
        ("Please confirm you would like to move forward assigning peer reviews for", 
        f"{colored(ASSIGNMENT.name, 'green')}{colored('. Please note - this will delete any existing peer reviews in ', 'blue')}{colored(ASSIGNMENT.name, 'green')}")
        ])

    _create_reverse_peer_reviews(ASSIGNMENT, students_dict, og_peer_reviews)

    # for each submission1249368
    # get the user id
    # get the list of reviewers

def _check_for_auto_submit(assignment, students):

    confirm = input(colored(f"Do you need to auto-submit for {assignment.name}? [y/n]: ", "blue"))

    confirm = confirm.upper()

    if confirm == "Y":
        auto_submit(students, assignment)

    elif confirm == "N":
        print("Not autosubmitting - please beware peer reviews only work for students with submissions")

    else: 
        print(f"Entered key {confirm} not valid. Please enter Y or N.")
        _check_for_auto_submit(assignment, students)

    

def _create_reverse_peer_reviews(assignment, student_dict, original_reviews):

    # arrange the original peer reviews so for each "assessor" there is a list of "user_ids"
    # the assessor in the previous round becomes the reviewer 
    # i.e) in round 1 Student A was reviewed by student B, C, D, E
    # B,C,D,E are assessors in round 1, in round 2 their feedback is assessed by A
    # Student A reviews B,C,D,E in this round

    new_peer_reviews = original_reviews.groupby("assessor_id")["user_id"].apply(list).reset_index()
    new_assignment_submissions = assignment.get_submissions()

    for i in new_assignment_submissions:
        to_review_list = None
        
        user_id = i.user_id
        reviewer_name = student_dict.get(int(user_id))
        
        # DELETE REVIEWS
        _delete_submission_peer_reviews(i)

        try:
            to_review = new_peer_reviews[new_peer_reviews['assessor_id'] == user_id]
            to_review_list = to_review.iloc[0]["user_id"]

        except:
            print(f"{reviewer_name} was not assigned to give any reviews")

        if to_review_list:
            print(f"{reviewer_name} is reviewed by {len(to_review_list)} students:")
            

            for j in to_review_list:
                reviewee_name = student_dict.get(int(j))
                try:
                    # for the submission (which is done by the user_id in i)
                    # create a peer review by k, where k is one of the reviewers
                    
                    i.create_submission_peer_review(j)
                    print(f"\t-{reviewee_name}")
                    
                except Exception as e:
                    print(f"Error {e}")


def _create_student_dict(students):
    students_dict = {}
    for student in students:
        student_dict = student.__dict__
        students_dict.update({student_dict.get("id"): student_dict.get("name")})
    return(students_dict)

def _get_peer_reviews(assignment):
    
    peer_reviews = assignment.get_peer_reviews()
    df = pd.DataFrame([i.__dict__ for i in peer_reviews])[["user_id", "assessor_id"]]
    return(df)


def _delete_submission_peer_reviews(submission):

    peer_reviews = submission.get_submission_peer_reviews()

    for pr in peer_reviews:
        delete_reviewer = pr.__dict__.get("assessor_id")
        submission.delete_submission_peer_review(delete_reviewer)

    return


if __name__ == "__main__":
    
    main()




    