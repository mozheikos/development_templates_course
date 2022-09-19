"""
Page controller module. To add controller for path - add tuple(path, callable) to urls
variable
"""


from views import index_view, contacts_view, address_view, education_view, programm_view, create_category, create_course

urls = [
    ('/', index_view),
    ('/contact/', contacts_view),
    ('/address/', address_view),
    # ('/education/', education_view),
    # ('/education/programm/', programm_view),
    # ('/education/add_category/', create_category),
    # ('/education/add_course/', create_course)
]
