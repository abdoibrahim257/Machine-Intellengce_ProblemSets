from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    std_id = student.id
    ttl_hrs: int = 0
    ttl_Points: float = 0.0
    for course in courses:
        if std_id in course.grades:
            #summing total number of hours
            ttl_hrs += course.hours
            #calculating the hrs*points
            ttl_Points += course.hours * course.convert_grade_to_points(course.grades[std_id])
    if ttl_hrs == 0:
        return 0.0
    else:
        return ttl_Points/ttl_hrs