#!/bin/python3

## NEED TO BE CHANGED
GITHUB_ORG = "csunibo"
FORGEJO_ORG = "csunibo"
FORGEJO_URL = "https://git.students.cs.unibo.it"

FORGEJO_API_ENDPOIN = "/api/v1/repos/migrate" # This is the default endpoint

import requests
import json
import os

def create_mirror(repo_url, repo_name, repo_owner, token_forgejo, token_github):
    api_url = FORGEJO_URL + FORGEJO_API_ENDPOIN
    headers = {
            'accept': 'application/json', 
            'Authorization': 'token ' + token_forgejo, 
            'Content-Type': 'application/json'
    }
    body = {
            'clone_addr': repo_url,
            'mirror': True,
            'private': False,
            'repo_name': repo_name,
            'repo_owner': repo_owner,
            'service': 'github',
            'auth_token': token_github
    }

    r = requests.post(api_url, headers=headers, data=json.dumps(body))
    if r.status_code == 409:
        print("WARNING: " + repo_name + " already exists!")
    elif r.status_code != 201:
        print("ERROR: during the mirrorin of " + repo_name)
        print(r.text)
    else:
        print("INFO: successfully created: " + repo_name)

def main():
    if "TOKEN_FORGEJO" not in os.environ:
        print("Please provide the forgejo token via the TOKEN_FORGEJO env variable")
        return -1 

    token_forgejo = os.environ.get("TOKEN_FORGEJO")

    if "TOKEN_GITHUB" not in os.environ:
        print("Please provide the github token via the TOKEN_GITHUB env variable")
        return -1 

    token_github = os.environ.get("TOKEN_GITHUB")

    url = 'https://api.github.com/orgs/' + GITHUB_ORG + '/repos'
    headers = {
            'Accept': 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'request',
            'Authorization': 'Bearer ' + token_github
            }
    params = {'per_page': '100', 'page': '1'}

    base_url = "https://github.com"
    repo_owner = FORGEJO_ORG

    # Need to know how many pages i need to get in order to get all the repos
    request_parsed = []
    print("Getting all the repos names")
    while True:
        request = requests.get(url, params=params, headers=headers)

        if request.status_code != requests.codes.ok:
            print("Errore durante la richiesta. Status code: " + 
                  str(request.status_code), end="")
            print(request.text)
            break
        else:
            request_parsed += json.loads(request.text)
            if not json.loads(request.text):
                break
            else:
                n = int(params.get('page'))
                n = n + 1
                params.update({'page': n})

    total_number = len(request_parsed)
    print("Fetched " + str(total_number) + " repos")
    print("Starting the mirroring")

    i = 1
    for repo in request_parsed:
        repo_name = repo["name"] 
        url = base_url + '/' + repo_owner + '/' + repo_name
        print('[' + str(i) + '/' + str(total_number) + '] ', end="")
        create_mirror(url, repo_name, repo_owner, token_forgejo, token_github)
        i = i + 1


if __name__ == "__main__":
    main()
