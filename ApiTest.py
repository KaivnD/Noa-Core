from Noa.Core import ApiTasker
from Noa.Hooks import before, after

class ApiTest(ApiTasker):
    
    @before('write')
    def open_file(self, *args):
        print(self.filename)
        self.file = open(self.filename, 'w')

    @after('write')
    def close_file(self, *args):
        print("Close")
        self.file.close()


ApiTest("testing.txt").write("This is a test.")