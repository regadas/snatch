import os
from core import GitSnatch


class Github(GitSnatch):

    def __init__(self, src):
        if not (src.startswith('http') or src.startswith('git')):
            src = os.path.join('https://github.com/%s', src)
        super(Github, self).__init__(src)
