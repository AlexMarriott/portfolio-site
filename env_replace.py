"""
This file is used for replacing the environment variables during the deployment stage. The variables are held in travis-ci for the repo.
This means that the env variables are not included on the website, reducing the security risk.
"""
from yaml import load, dump, Loader, YAMLError
import os
import fileinput
with open("docker-compose.yaml", 'r') as stream:
    try:
        loaded = load(stream, Loader=Loader)
    except Exception as exc:
        print(exc)

# Modify the fields from the dict
for i in loaded['services']['mongo']['environment']:
    loaded['services']['mongo']['environment'][i] = os.environ[i]


# Save it again
with open("app.yaml", 'w') as stream:
    try:
        dump(loaded, stream, default_flow_style=False)
    except YAMLError as exc:
        print(exc)

#Replace variables in javascript file.
with open('mongo-init.js', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('MONGO_INITDB_ROOT_PASSWORD', os.environ['MONGO_INITDB_ROOT_PASSWORD'])

# Write the file out again
with open('mongo-init.js', 'w') as file:
  file.write(filedata)