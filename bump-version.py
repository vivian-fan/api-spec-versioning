#!/bin/python


import git

import sys

import os

import  re

import shutil

import yaml

def bump_version(data, change):
    version = data['info']['version']
    next_version = str(version).split('\\.')
    i = 0
    for x in next_version:
        next_version[i] = int(x)
        i = i+1
    if change.lower() == 'minor':
        next_version[1] = next_version[1] + 1
        final_version =''
        for x in next_version:
            final_version = final_version+'.'+str(x)
        return final_version[1:len(final_version)]
    else:
        next_version[0] = next_version[0] + 1
        next_version[1] = 0
        next_version[2] = 0
        final_version =''
        for x in next_version:
            final_version = final_version+'.'+str(x)
        return final_version[1:len(final_version)]

def calculate_final_version(master_version, calculated_version):
    master = str(master_version).split("\\.")
    calculated = str(calculated_version).split("\\.")
    final = master
    i = 0
    while i < len(master):
        if calculated[i] > master[i]:
            final = calculated
        i = i+1
    final_version = ''
    for x in final:
        final_version = final_version+'.'+x
    return final_version[1:len(final_version)]


change = sys.argv[1]

access_token = sys.argv[2]



spec_file_name = 'petstore.yml'

release_path = './release'

master_path = './master'

if os.path.exists(release_path):
    shutil.rmtree(release_path)

if os.path.exists(master_path):
    shutil.rmtree(master_path)


os.mkdir(release_path)

os.mkdir(master_path)

repo_url = 'https://'+access_token+':x-oauth-basic@github.com/kinturi/api-spec-versioning.git'

clone_repo_master = git.Repo.clone_from(repo_url,master_path,branch='master')

release_branches = []

for branch in clone_repo_master.refs:
    if re.search('production-release',branch.__str__()) is not None:
        release_branches.append(branch.__str__())

if release_branches is not None:
    release_branches.sort()

clone_repo_release = git.Repo.clone_from(repo_url,release_path,branch=release_branches[len(release_branches)-1])

master_branch_spec = {}

with open(master_path+'/'+spec_file_name, 'r') as master_branch_spec:
    master_branch_spec = yaml.safe_load(master_branch_spec)


release_branch_spec = {}

with open(release_path+'/'+spec_file_name, 'r') as release_branch_spec:
    release_branch_spec = yaml.safe_load(release_branch_spec)

calculated_version = bump_version(release_branch_spec,change)

final_version = calculate_final_version(master_branch_spec['info']['version'],release_branch_spec['info']['version'])

shutil.rmtree(release_path)

shutil.rmtree(master_path)

if master_branch_spec['info']['version'] != final_version:
    os.remove(spec_file_name)
    master_branch_spec['info']['version'] = final_version
    with open(spec_file_name, "w+") as f:
        f.write(yaml.safe_dump(master_branch_spec,default_flow_style=False, sort_keys=False))


















