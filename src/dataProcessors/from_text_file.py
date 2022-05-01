

class RWDataFromTextFile:
    def __init__(self):
        self.filename = "src/dataProcessors/replied_mention_id.txt"

    def open_file(self):
        with open(self.filename, 'r') as f:
            last_line = f.readlines()[-1]
        return last_line

    def update_file(self, value):
        with open(self.filename, 'w') as f:
            f.write("%s\n" % value)
