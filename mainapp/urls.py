"""
Page controller module. To add controller for path - add tuple(path, callable) to urls
variable
"""


from mainapp.views import index_view, contacts_view, ViewCourse, StudentsList, \
    CreateStudent, StudentProfile, EditCourse

urls = [
    ('/', index_view),
    ('/contact/', contacts_view),
    ('/education/register/', CreateStudent()),
    ('/education/course_detail/', ViewCourse()),
    ('/education/edit_course/', EditCourse()),
    ('/students/', StudentsList()),
    ('/students/profile/', StudentProfile())
]
