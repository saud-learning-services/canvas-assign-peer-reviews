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
    new_peer_reviews = og_peer_reviews.groupby("user_id")["assessor_id"].apply(list).reset_index()

    # for the new assignment, delete any existing peer reviews
    #TODO - add confirmation step here 
    # returns submissions, needed to assign new peer reviews
    new_assignment_submissions = _delete_any_existing_peer_reviews(ASSIGNMENT)

    # for each submission
    # get the user id
    # get the list of reviewers
    for i in new_assignment_submissions:
        reviewed_by_list = None
        user_id = i.user_id
        reviewer_name = students.get(int(user_id))
        
        try:
            reviewed_by = new_peer_reviews[new_peer_reviews['user_id'] == user_id]
            reviewed_by_list = reviewed_by.iloc[0]["assessor_id"]
        except:
            print(f"{reviewer_name} was not assigned to any reviewers")
            

        if reviewed_by_list:
            print(f"{reviewer_name} reviewing {len(reviewed_by_list)} reviewers:")
            for j in reviewed_by_list:
                reviewee_name = students.get(int(j))
                try:
                    # for the submission (which is done by the user_id in i)
                    # create a peer review by k, where k is one of the reviewers
                    ASSIGNMENT.get_submission(j).create_submission_peer_review(j)
                    print(f"\t-{reviewee_name}")
                except:
                    print(f"Error creating review by {user_id} for {reviewee_name}")


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


def _delete_any_existing_peer_reviews(assignment):

    submissions = assignment.get_submissions()
    
    for i in submissions:
        peer_review = i.get_submission_peer_reviews()

        for j in peer_review:
            delete_reviewer = j.__dict__.get("assessor_id")
            i.delete_submission_peer_review(delete_reviewer)

    return(submissions)
    print(f"Deleted all submissions for {assignment.name}")

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
    