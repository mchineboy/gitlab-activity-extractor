# File: src/gitlab_api.py
import requests
from time import sleep
from typing import List, Dict, Any
import sys


class GitLabAPI:
    def __init__(
            self, private_token: str, gitlab_url: str = "https://gitlab.com",
            debug: bool = False):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.headers = {'PRIVATE-TOKEN': private_token}
        self.debug = debug

    def debug_print(self, message: str):
        """Print debug messages if debug mode is enabled."""
        if self.debug:
            print(f"DEBUG: {message}")

    def test_authentication(self) -> bool:
        """Test if the token has correct permissions."""
        url = f"{self.gitlab_url}/api/v4/user"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print(f"Successfully authenticated as: {response.json()['name']}")
            return True
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def get_group_info(self, group_id: int) -> Dict[str, Any]:
        """Get group information to verify access."""
        url = f"{self.gitlab_url}/api/v4/groups/{group_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error accessing group {group_id}: {str(e)}")
            sys.exit(1)

    def get_group_projects(self, group_id: int) -> List[Dict[str, Any]]:
        """Get all projects in a group and its subgroups."""
        projects = []
        page = 1
        while True:
            url = f"{self.gitlab_url}/api/v4/groups/{group_id}/projects"
            params = {
                'page': page,
                'per_page': 100,
                'include_subgroups': True,
                'archived': False,
                'simple': False
            }
            try:
                response = requests.get(
                    url, headers=self.headers, params=params)
                response.raise_for_status()
                batch = response.json()
                if not batch:
                    break
                projects.extend(batch)
                page += 1
                sleep(0.5)
            except Exception as e:
                print(f"Error fetching projects page {page}: {str(e)}")
                break
        return projects

    def get_project_commits(self, project: Dict[str, Any],
                            since: str = "",
                            author_email: str = "") -> List[Dict[str, Any]]:
        """Get all commits for a specific project."""
        commits = []
        page = 1

        while True:
            url = f"{
                self.gitlab_url}/api/v4/projects/{project['id']}/repository/commits"  # noqa
            params = {
                'page': page,
                'per_page': 100,
                'with_stats': True,
                'all': True
            }
            if since:
                params['since'] = since
            if author_email:
                params['author'] = author_email

            try:
                response = requests.get(
                    url, headers=self.headers, params=params)
                response.raise_for_status()
                batch = response.json()

                if page == 1 and batch:
                    print(f"First commit: {batch[0]['id']}")
                if not batch:
                    break

                commits.extend(batch)
                page += 1
                sleep(0.5)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Project {project['path_with_namespace']} (ID: {
                          project['id']}) not found or no access.")
                else:
                    print(f"HTTP Error for project {
                          project['path_with_namespace']}: {str(e)}")
                break
            except Exception as e:
                print(f"Error fetching commits for project {
                      project['path_with_namespace']}: {str(e)}")
                break

        return commits
