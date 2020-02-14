import re
import sys
import json
from pathlib import Path

# the  syntax r'some string' means that we are creating a raw string, and all
# the characters written need to be interpreted as they appear. Otherwise, we
# would need to put double backslashes in our regular expressions, making our
# string less readable.
# Look that the pattern have two groups
DIRECTIVE_RE = re.compile(
r'/\*\*\s*(include|variable|loopover|endloop|loopvar)'
r'\s*([^ *]*)\s*\*\*/')

class TemplateEngine:
    def __init__(self, infilename, outfilename, contextfilename):
        with open(infilename) as input_file:
            self.template = input_file.read()
        
        self.working_dir = Path(infilename).absolute().parent
        
        # current char in the content we are processing
        self.pos = 0
        
        # open file 'outfilename' to write
        self.outfile = open(outfilename, 'w')
        
        # load from 'contextfile'
        with open(contextfilename) as contextfile:
            self.context = json.load(contextfile)
    
    def __del__(self):
        self.outfile.close()
    
    def process(self):
        # look  if  'self.template'  matches the  'DIRECTIVE_RE'  pattern. The
        # difference using 're.compile' is that we can use the 'pos' to search
        # just since a specific position.
        match = DIRECTIVE_RE.search(self.template, pos=self.pos)
        while match:
            # These  statements find the first string that matches the regex
            # and  outputs  everything  from  the  current  position  to the
            # match.start() and advances  the position through 'method_name' 
            # that  will  handle  the  'directive'  correctly.  Writes  from
            # 'self.template' to 'self.outfile'
            self.outfile.write(self.template[self.pos:match.start()])
            
            # 'match.groups()' will return all the groups matched, in this case
            # two  groups:  one  containing  the  directive name e another with
            # the directive argument.
            directive, argument = match.groups()
            method_name = 'process_{}'.format(directive)
            
            # Call the appropriate class attribute inside the current object.
            getattr(self, method_name)(match, argument)
            
            # Look for more patterns
            match = DIRECTIVE_RE.search(self.template, pos=self.pos)
        self.outfile.write(self.template[self.pos:])
    
    # the '/' operator concatenates the string '/argument' at
    # 'self.working_dir'.
    def process_include(self, match, argument):
        with (self.working_dir / argument).open() as includefile:
            self.outfile.write(includefile.read())
            self.pos = match.end()
    
    def process_variable(self, match, argument):
        self.outfile.write(self.context.get(argument, ''))
        self.pos = match.end()
    
    def process_loopover(self, match, argument):
        self.loop_index = 0
        self.loop_list = self.context.get(argument, [])
        self.pos = self.loop_pos = match.end()
    
    def process_loopvar(self, match, argument):
        self.outfile.write(self.loop_list[self.loop_index])
        self.pos = match.end()
    
    def process_endloop(self, match, argument):
        self.loop_index += 1
        if self.loop_index >= len(self.loop_list):
            self.pos = match.end()
            del self.loop_index
            del self.loop_list
            del self.loop_pos
        else:
            self.pos = self.loop_pos    

if __name__ == '__main__':
    infilename, outfilename, contextfilename = sys.argv[1:]
    engine = TemplateEngine(infilename, outfilename, contextfilename)
    engine.process()