# File: src/main.py
import os
import sys
from datetime import datetime
import argparse
from typing import Dict, Any
from .gitlab_api import GitLabAPI
from .ai_summarizer import CommitSummarizer
from .data_processor import ActivityDataProcessor
from .report_generator import ReportGenerator


def parse_args() -> Dict[str, Any]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Extract and analyze GitLab repository activity'
    )

    # Required arguments
    parser.add_argument(
        '--token',
        help='GitLab API token',
        default=os.getenv('GITLAB_TOKEN')
    )
    parser.add_argument(
        '--group-id',
        type=int,
        help='GitLab group ID to analyze',
        default=os.getenv('GITLAB_GROUP_ID')
    )

    # Optional arguments with defaults
    parser.add_argument(
        '--gitlab-url',
        default=os.getenv('GITLAB_URL', 'https://gitlab.com'),
        help='GitLab instance URL (default: https://gitlab.com)'
    )
    parser.add_argument(
        '--author-email',
        default=os.getenv('GITLAB_AUTHOR_EMAIL', ''),
        help='Filter commits by author email'
    )
    parser.add_argument(
        '--minutes-per-commit',
        type=int,
        default=int(os.getenv('MINUTES_PER_COMMIT', '15')),
        help='Estimated minutes spent per commit (default: 15)'
    )
    parser.add_argument(
        '--output-prefix',
        default=os.getenv('OUTPUT_PREFIX', 'gitlab_activity'),
        help='Prefix for output files (default: gitlab_activity)'
    )
    parser.add_argument(
        '--start-date',
        type=lambda s: datetime.strptime(s, '%Y-%m-%d').isoformat(),
        default=os.getenv('START_DATE', '2024-08-12'),
        help='Start date for commit history (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--openai-key',
        default=os.getenv('OPENAI_API_KEY'),
        help='OpenAI API key for commit summarization'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=os.getenv('DEBUG', '').lower() == 'true',
        help='Enable debug output'
    )

    args = parser.parse_args()

    # Validate required arguments
    if not args.token:
        parser.error(
            "GitLab token is required. Provide via --token or GITLAB_TOKEN environment variable")  # noqa
    if not args.group_id:
        parser.error(
            "Group ID is required. Provide via --group-id or GITLAB_GROUP_ID environment variable")  # noqa

    return vars(args)


def main():
    # Parse command line arguments
    config = parse_args()

    # Initialize components
    gitlab = GitLabAPI(
        private_token=config['token'],
        gitlab_url=config['gitlab_url'],
        debug=config['debug']
    )

    summarizer = CommitSummarizer(
        config['openai_key']) if config['openai_key'] else None
    processor = ActivityDataProcessor(summarizer)
    reporter = ReportGenerator(config['output_prefix'])

    try:
        if not gitlab.test_authentication():
            print("\nPlease ensure your token has the following scopes:")
            print("- api")
            print("- read_repository")
            print("- read_user")
            sys.exit(1)

        # Fetch and process data
        group_info = gitlab.get_group_info(config['group_id'])
        print(f"\nAccessing group: {group_info['full_name']}")

        projects = gitlab.get_group_projects(config['group_id'])
        print(f"Found {len(projects)} projects in group {config['group_id']}")

        if not projects:
            print("No projects found. Please check group ID and permissions.")
            sys.exit(1)

        # Collect commits
        all_commits = []
        successful_projects = 0

        for project in projects:
            try:
                commits = gitlab.get_project_commits(
                    project,
                    config['start_date'],
                    config['author_email']
                )
                if commits:
                    print(f"Found {len(commits)} commits in {project['path_with_namespace']}")  # noqa
                    successful_projects += 1
                    for commit in commits:
                        all_commits.append({
                            'timestamp': commit['created_at'],
                            'project': project['path_with_namespace'],
                            'commit_id': commit['id'],
                            'message': commit['message'],
                            'additions': commit.get('stats', {}).get('additions', 0),  # noqa
                            'deletions': commit.get('stats', {}).get('deletions', 0),  # noqa
                            'total_changes': commit.get('stats', {}).get('total', 0),  # noqa
                            'author_name': commit['author_name'],
                            'author_email': commit['author_email']
                        })
            except Exception as e:
                print(f"Error processing project {
                      project['path_with_namespace']}: {str(e)}")

        print(f"\nSuccessfully accessed {successful_projects} out of {len(projects)} projects")  # noqa

        if not all_commits:
            print("\nNo commits found matching the criteria")
            return

        # Process commits and generate reports
        commits_df, repo_stats = processor.process_commits(
            all_commits,
            config['minutes_per_commit']
        )
        reporter.generate_reports(commits_df, repo_stats)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if summarizer:
            summarizer.cleanup()


if __name__ == '__main__':
    main()
