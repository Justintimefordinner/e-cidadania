#/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import subprocess

"""
This script installs a development environment in an easy way, instead of
having to execute all the bootstrapping commands.
"""

__version__ = '0.2'
print("e-cidadania install script %s\n" % __version__)

# Detect where is this file
cwd = os.path.dirname(os.path.realpath(__file__))
# Change the working dir
os.chdir(cwd)

# Execute the bootstrap
print(" * Bootstrapping...")
a = subprocess.run('python bootstrap.py', shell=True)

print(" * Making buildout...")
b = subprocess.run('bin/buildout', shell=True)

d = input(' * Do you want to create the database? (y/n) ')

if d.lower() == 'y':
	os.chdir(os.path.join(cwd, 'src'))
	c = subprocess.run('../bin/django syncdb', shell=True)
elif d.lower() == 'n':
	print('Process finished')
	print("""You should follow this instructions blablabla""")
else:
	sys.exit(0)