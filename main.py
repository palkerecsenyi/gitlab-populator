import os

import gitlab
import lorem
from tqdm import tqdm


def main():
    token = os.getenv("GITLAB_TOKEN")
    url = os.getenv("GITLAB_URL")
    group_name = os.getenv("GITLAB_GROUP")
    generator_fingerprint = os.getenv("GITLAB_GENERATOR_FINGERPRINT")
    num_repos = os.getenv("GITLAB_NUM_REPOS")
    assert token is not None
    assert url is not None
    assert group_name is not None
    assert generator_fingerprint is not None
    assert num_repos is not None

    num_repos = int(num_repos)

    gl = gitlab.Gitlab(url=url, private_token=token)
    gl.auth()

    group = gl.groups.get(group_name)
    for proj in tqdm(group.projects.list(iterator=True), desc="delete"):
        if not proj.path.startswith(f"{generator_fingerprint}-"):
            continue

        # You need to "mark" the project for deletion first which sets a timer
        gl.projects.delete(proj.id)
        # ...and then we skip the timer by forcing an immediate deletion
        proj = gl.projects.get(proj.id)
        gl.projects.delete(
            proj.id, full_path=proj.path_with_namespace, permanently_remove=True
        )

    for i in tqdm(range(num_repos), desc="create"):
        path = f"{generator_fingerprint}-{lorem.get_word()}-{i}"

        gl.projects.create(
            {
                "path": path,
                "namespace_id": group.id,
                "initialize_with_readme": True,
                "description": "Managed by gitlab-populator",
            }
        )


if __name__ == "__main__":
    main()
