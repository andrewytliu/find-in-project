"""
    Parse the result of ack into html
"""

import subprocess
import cgi
import re

class FindInProjectParser:

    def __init__(self, query, path):
        arg = ['ack-grep', '-C', '2', '--color','--color-filename=reset', '--color-match=yellow', query]
        process = subprocess.Popen(arg, stdout=subprocess.PIPE, cwd=path)
        self.raw = cgi.escape(process.communicate()[0])
        #print self.raw

    def html(self):
        blocks = self.__tuple()
        result = ""
        if len(blocks[0]) == 0:
            return result
        for block in blocks:
            table = """
<table>
    <colgroup class="line-number"></colgroup>
    <colgroup class="code"></colgroup>
    <thead onclick="javascript:toggle(this)">
        <tr>
            <td class="filename" colspan="2"><span class="open">&#9660;</span> %s</td>
        </tr>
    </thead>
    <tbody>
            """ % block[0][0]
            for line in block:
                matchclass = ""
                if line[2]:
                    matchclass = ' match'
                table += """
        <tr onclick="javascript:goto('%s', %s)">
            <td class="line-number%s">%s</td>
            <td class="code%s">%s</td>
        </tr>
                """ % (line[0], line[1], matchclass, line[1], matchclass, line[3])
            table += """
    </tbody>
</table>
            """
            result += table
        return result

    def __tuple(self):
        #\x1b[0mew\x1b[0m-64-
        #\x1b[0mew\x1b[0m-65-
        #\x1b[0mew\x1b[0m:66:if __name__ == "\x1b[33m__main__\x1b[0m":\x1b[0m\x1b[K
        #\x1b[0mew\x1b[0m-67-    Eastwind()
        #\x1b[0mew\x1b[0m-68-

        # strip empty highlight
        process = self.raw.replace('\x1b[0m\x1b[K','')
        groups = process.split('--')
        lines = [[self.__metadata(l) for l in g.split('\n') if l != ''] for g in groups]
        return lines

    def __metadata(self, line):
        match = re.match("^\\x1b\[0m(.*?)\\x1b\[0m[:-](\d+)([:-])(.*)", line)
        matched = (match.group(3) == ':')
        clear = match.group(4).replace(' ', '&nbsp;')
        clear = re.sub("\\x1b\[33m(.*?)\\x1b\[0m", '<span class="highlight">\\1</span>', clear)
        return (match.group(1), match.group(2), matched, clear)

