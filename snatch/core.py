import logging
import os
import mimetypes
from ConfigParser import RawConfigParser
from tempfile import mkdtemp
from git import Repo
from string import Template
from shutil import move, rmtree
from glob import iglob
from cStringIO import StringIO

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('snatch')


class Snatch(object):
    _properties_ini = 'properties.ini'
    _section = 'props'

    def __init__(self, src):
        self.src = src
        self.clone()
        self.load_properties()

    def clone(self):
        raise NotImplementedError

    def load_properties(self):
        config = RawConfigParser()
        config.read(os.path.join(self.local_src, self._properties_ini))
        self.properties = dict(config.items(self._section))
        return self.properties

    def generate_in(self, dst):

        dst = dst or os.getcwd()

        def _template(content):
            try:
                content = Template(content).substitute(**self.properties)
            except:
                logger.exception("missing property")

            return content

        def _walk(path):
            for path in iglob(path):
                new_path = _template(path)
                os.rename(path, new_path)
                if os.path.isdir(new_path):
                    _walk(os.path.join(new_path, '*'))
                else:
                    mt, _ = mimetypes.guess_type(new_path)
                    if not mt or mt.startswith('text'):
                        content = StringIO()
                        with open(new_path, 'r') as FILE:
                            content.write(_template(FILE.read()))
                        with open(new_path, 'w') as FILE:
                            FILE.write(content.getvalue())

        _walk(os.path.join(self.local_src, '*'))
        move(self.local_src, os.path.join(dst, self.properties.get('name')))
        self.clean(dst)


class GitSnatch(Snatch):
    def clone(self, dst=None):
        self.local_src = dst or mkdtemp()
        Repo.clone_from(self.src, self.local_src)
        return self.local_src

    def clean(self, dst):
        rmtree(os.path.join(dst, '.git'))
