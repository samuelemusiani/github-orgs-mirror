#!/bin/python3

import requests
import json
import os

def create_mirror(repo_url, repo_name, repo_owner, token):
    api_url = 'https://git.students.cs.unibo.it/api/v1/repos/migrate'
    headers = {
            'accept': 'application/json', 
            'Authorization': 'token ' + token, 
            'Content-Type': 'application/json'
    }
    body = {
            'clone_addr': repo_url,
            'mirror': True,
            'private': False,
            'repo_name': repo_name,
            'repo_owner': repo_owner,
            'service': 'github',
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

    token = os.environ.get("TOKEN_FORGEJO")

    url = 'https://api.github.com/orgs/csunibo/repos'
    headers = {
            'Accept': 'application/vnd.github+json', 
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'request'
            }
    params = {'per_page': '100', 'page': '2'}

    base_url = "https://github.com"
    repo_owner = "csunibo"

    return 1

    # create_mirror(url, repo_name, repo_owner)

# Need to know how many pages i need to get in order to get all the repos
    request_parsed = []
    # while True:
    #     request = requests.get(url, params=params, headers=headers)
    #
    #     if request.status_code != requests.codes.ok:
    #         print("Errore durante la richiesta")
    #         print(request.status_code)
    #         break
    #     else:
    #         request_parsed += json.loads(request.text)
    #         if not request_parsed:
    #             print("Finito")
    #             break
    #         else:
    #             n = int(params.get('page'))
    #             n = n + 1
    #             params.update({'page': n})



    # print(request_parsed)
    # for repo in request_parsed:
    #     print(repo["full_name"])

    f = open("repos.txt", "r")
    names = f.readlines()

    total_number = len(names)
    i = 1
    for n in names:
        repo_name = n.strip()
        url = base_url + '/' + repo_owner + '/' + repo_name
        print('[' + str(i) + '/' + str(total_number) + '] ', end="")
        create_mirror(url, repo_name, repo_owner)
        i = i + 1

    f.close()


if __name__ == "__main__":
    main()
