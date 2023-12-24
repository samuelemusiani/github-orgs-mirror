Simple python scrypt to mirror al the repositories of a github organization on 
forgejo.

In order to create repos on forgejo you must provide an access token. You can 
get one via the webui. In order to use it on the script you must set the 
`TOKEN_FORGEJO` variable:

```bash
export TOKEN_FORGEJO=...
```

In order fetch more results from github you need an access token. Export it like
the forgejo token:
```bash
export TOKEN_GITHUB=...
```

There are some values that need to be changed in the header of the scritp, like
`GITHUB_ORG`, `FORGEJO_ORG`, `FORGEJO_URL` and `FORGEJO_API_ENDPOIN`.

