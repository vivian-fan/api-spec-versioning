#!/bin/python


import git

import os

import  re

repo = git.Repo(".")


release_branches = []

for branch in repo.refs:
    if re.search('production-release',branch.__str__()) is not None:
        release_branches.append(branch.__str__())

if release_branches is not None:
    release_branches.sort()

os.mkdir('./release')

os.mkdir('./master')











