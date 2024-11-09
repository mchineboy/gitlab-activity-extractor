# File: src/data_processor.py
import pandas as pd
from typing import Dict, Tuple, List, Optional
from .ai_summarizer import CommitSummarizer


class ActivityDataProcessor:
    def __init__(self, summarizer: Optional[CommitSummarizer] = None):
        self.summarizer = summarizer

    def process_commits(
        self, commits: List[Dict],
        minutes_per_commit: int = 15
    ) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Process commit data and calculate statistics by repository."""
        if not commits:
            return pd.DataFrame(), {}

        # Create DataFrame from commits
        commits_df = pd.DataFrame(commits)
        commits_df['timestamp'] = pd.to_datetime(
            commits_df['timestamp'], utc=True)
        commits_df = commits_df.sort_values('timestamp')

        # Calculate activity times
        commits_df['activity_minutes'] = minutes_per_commit
        commits_df['activity_start'] = commits_df['timestamp'] - \
            pd.Timedelta(minutes=minutes_per_commit)
        commits_df['activity_end'] = commits_df['timestamp']
        commits_df['date'] = commits_df['timestamp'].dt.date

        # Group by repository and calculate stats
        repo_stats = {}
        for repo_name, repo_commits in commits_df.groupby('project'):
            daily_stats = repo_commits.groupby('date').agg({
                'commit_id': 'count',
                'activity_minutes': 'sum',
                'additions': 'sum',
                'deletions': 'sum',
                'total_changes': 'sum',
                'message': list
            }).reset_index()

            # Generate AI summaries if available
            if self.summarizer:
                daily_stats['commit_summary'] = daily_stats['message'].apply(
                    self.summarizer.summarize_commits)
            else:
                daily_stats['commit_summary'] = "AI summarization not available"  # noqa

            daily_stats.columns = [
                'date', 'commits', 'activity_minutes',
                'additions', 'deletions', 'total_changes',
                'commit_messages', 'commit_summary'
            ]

            repo_stats[repo_name] = daily_stats

        return commits_df, repo_stats
