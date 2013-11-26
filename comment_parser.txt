import re
import sys

text = sys.stdin.read()

def comment_parser(text, comments=True):
    comm = []
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            comm.append(s)
            return ""
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    code = re.sub(pattern, replacer, text)
    if comments: return '\n'.join(comm)
    else: return code

print(comment_parser(text))
