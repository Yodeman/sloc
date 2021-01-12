import os, sys

class Lines_Sloc():
    """
    Calculate the total numbers of lines and total
    sloc of files at and below a given directory.
    """
    def __init__(self, start_dir, dependencies=[]):
        self.start = start_dir
        self.dependencies = dependencies
        self.vfiles = 0
        self.exts = {}

    def folder_explorer(self):
        """
        Traverses through folders and calls file_traverser on
        files in the folder.
        """
        for (thisDir, subDir, filesHere) in os.walk(self.start):
            for file in filesHere:
                fpath = os.path.join(thisDir, file)
                self.file_traverser(fpath)

    def file_traverser(self, fpath):
        """
        Reads the file and then compute the total numbers of lines
        and the total sloc.

        fpath - file path.
        """
        self.vfiles += 1
        
        try:
            exts = os.path.splitext(fpath)[1]
            with open(fpath) as f:
                doc = f.readlines()
                lines = len(doc)
                sloc = len([i for i in doc if not i.isspace()])
            if exts in self.dependencies:
                print(f'\nSkipping {fpath}\n')
            elif exts in self.exts:
                self.exts[exts]['lines'] += lines
                self.exts[exts]['sloc'] += sloc
            elif exts not in self.exts:
                self.exts[exts] = {'lines':lines, 'sloc':sloc}
        except:
            print(f'Error while attempting to read {fpath}.\nError_info: {sys.exc_info()}\n')

    def run(self):
        self.folder_explorer()
        print(f"Visited {self.vfiles} files.")
        for i in self.exts:
            print(f"{i}: total lines --> {self.exts[i]['lines']}\ttotal sloc --> {self.exts[i]['sloc']}")

if __name__ == "__main__":
    start_dir = input('Enter the starting directory: ')
    dependencies = input('What file extensions will you like exclude? ').split()
    line_sloc =Lines_Sloc(start_dir, dependencies)
    line_sloc.run()