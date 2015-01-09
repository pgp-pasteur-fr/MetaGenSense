
def add_project( request ):
    
    return {'current_project':request.session.get('current_project')}
            