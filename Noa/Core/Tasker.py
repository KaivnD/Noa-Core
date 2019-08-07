from Noa.Hooks import Hook

class ApiTasker(object):
    
    def __init__(self, filename):
        self.file = None
        self.filename = filename

    @Hook
    def write(self, text):
        self.file.write(text)