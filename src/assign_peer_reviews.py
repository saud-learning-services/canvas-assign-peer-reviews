import pandas as pd
from helpers import auto_submit
from interface import get_user_inputs, _prompt_for_confirmation
import os
from dotenv import load_dotenv
import settings
load_dotenv() 

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def setup(API_URL, API_KEY):
    
    # get the user inputs
    # this creates necessary settings variables
    get_user_inputs(API_URL, API_KEY)
    
    COURSE = settings.COURSE
    ASSIGNMENT = settings.ASSIGNMENT
    PR_SOURCE = settings.PR_SOURCE
    ASSIGNMENT_PR = settings.ASSIGNMENT_PR
    
    #TODO - implement the group option
    GROUP_PR = settings.GROUP_PR 

    # get the studetns in the course
    students = _create_student_dict(COURSE)
    
    # get the peer reviews from the original assignment
    og_peer_reviews = _get_peer_reviews(ASSIGNMENT_PR)

    # for each user, get the list of who they were assessed by
    # in the new peer reviews, the user will assess the original assessees
    
    # for the new assignment, delete any existing peer reviews
    #TODO - add confirmation step here 
    # returns submissions, needed to assign new peer reviews

    _prompt_for_confirmation([("Please confirm you would like to move forward assigning peer reviews for: ", f"{ASSIGNMENT.name}. Please note - this will delete any existing peer reviews in {ASSIGNMENT.name}")])
    _create_reverse_peer_reviews(ASSIGNMENT, students, og_peer_reviews)

    # for each submission
    # get the user id
    # get the list of reviewers


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


def _create_student_dict(course):
    students = course.get_users(enrollment_type=["student"])
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
    