"""
    Parse the result of ack into html
"""

import subprocess

class FindInProjectParser:

    def __init__(self, query, path):
        self.raw = subprocess.Popen(['ack-grep', '-C', '2', query], stdout=subprocess.PIPE, cwd=path)

    def html(self):
        # strip empty highlight
        process = self.raw.replace('\x1b[0m\x1b[K','')
        # highlight with span
        process = re.sub("\\x1b\[30;43m(.*)\\x1b\[0m", '<span class="highlight>\\1</span>', process)
#\x1b[1;32mew\x1b[0m-64-
#\x1b[1;32mew\x1b[0m-65-
#\x1b[1;32mew\x1b[0m:66:if __name__ == "\x1b[30;43m__main__\x1b[0m":\x1b[0m\x1b[K
#\x1b[1;32mew\x1b[0m-67-    Eastwind()
#\x1b[1;32mew\x1b[0m-68-

