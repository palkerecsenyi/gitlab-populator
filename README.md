# Gitlab Populator

Create `N` projects in a specific GitLab group automatically for testing purposes.

To use this application, install the dependencies and specify the following environment variables:

```
GITLAB_TOKEN="<GitLab personal access token>"
GITLAB_URL="<URL of your GitLab instance>"
GITLAB_GROUP="<path of group to add projects to>"
GITLAB_GENERATOR_FINGERPRINT="<a prefix to add to project names>"
GITLAB_NUM_REPOS="<number of repos to generate>"
```

When running, all repos with the `GITLAB_GENERATOR_FINGERPRINT` prefix will be deleted first and then new ones created in their place.
