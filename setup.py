#!/usr/bin/env python

from distutils.core import setup

setup(name='git-update-server',
      version='0.21',
      description='HTTP server to handle POST notifications of updated repositories on GitHub and BitBucket.',
      author='Andrew Naoum',
      author_email='andy.naoum@gmail.com',
      url='https://github.com/anaoum/git-update-server',
      packages=['git_update_server'],
      scripts=['git-update-server']
)
