@request.restful()
def api():
    def GET(*args,**vars):
        return dict()
    def POST(*args,**vars):
        return dict()
    def PUT(*args,**vars):
        return dict()
    def DELETE(*args,**vars):
        return dict()
    return locals()