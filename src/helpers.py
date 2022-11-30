from canvasapi import Canvas
import util
import sys

def create_instance(API_URL, API_KEY):
    try:
        canvas = Canvas(API_URL, API_KEY)
        util.print_success("Token Valid: {}".format(str(canvas.get_user('self'))))
        return(canvas)
    except Exception as e:
        util.print_error("\nInvalid Token: {}\n{}".format(API_KEY, str(e)))
        sys.exit(1)
        #raise

def _get_course(canvas_obj, course_id):
    '''
    Get Canvas course using canvas object from canvasapi
    Parameters:
        course (Canvas): canvasapi instance
        course_id (int): Canvas course ID
    Returns:
        canvasapi.course.Course object
    '''
    try:
        course = canvas_obj.get_course(course_id)
        util.print_success(f'Entered id: {course_id}, Course: {course.name}.')
    except Exception:
        util.shut_down(f'ERROR: Could not find course [ID: {course_id}]. Please check course id.')

    return course

def _matches_dict_key_val(dic, key, matches_val):
    '''Returns the dictionary if the provided key matches the match_val
    
    parameters:
        dic (dict)
        key (string): the key string in the dict to find
        matches_val (str|int): they str or int to try to find in the key

    returns:
        boolean
    '''
    # for use in list , example:
    # [d for d in list if _matches_dict_id(d, "key", matches_val)]
    return(dic[f"{key}"] == matches_val)
    
def _matches_dict_key_val_list(dic, key, matches_val_list):
    '''Returns the dictionary if the provided key matches the match_val
    
    parameters:
        dic (dict)
        key (string): the key string in the dict to find
        matches_val (str|int): they str or int to try to find in the key

    returns:
        boolean
    '''
    # for use in list , example:
    # [d for d in list if _matches_dict_id(d, "key", matches_val)]
    return(dic[f"{key}"] in matches_val_list)

def _return_single_dict_match(some_list, match_key, match_val):
            out = [d for d in some_list if _matches_dict_key_val(d, match_key, match_val)][0]
            return(out)
