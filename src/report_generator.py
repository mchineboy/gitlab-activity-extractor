# File: src/report_generator.py
import os
import pandas as pd
from typing import Dict
from datetime import datetime


class ReportGenerator:
    def __init__(self, output_prefix: str):
        self.output_dir = f"{output_prefix}_by_repo"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_reports(self, commits_df: pd.DataFrame, repo_stats: Dict[str, pd.DataFrame]):  # noqa
        """Generate all report files."""
        self._export_detailed_data(commits_df)
        self._export_daily_summaries(repo_stats)
        self._create_overall_summary(repo_stats)

    def _export_detailed_data(self, commits_df: pd.DataFrame):
        """Export detailed commit data by repository."""
        for repo_name, repo_commits in commits_df.groupby('project'):
            safe_repo_name = str(repo_name).replace('/', '_')
            repo_commits.to_csv(
                f"{self.output_dir}/{safe_repo_name}_detailed.csv",
                index=False
            )

    def _export_daily_summaries(self, repo_stats: Dict[str, pd.DataFrame]):
        """Export daily summaries and reports for each repository."""
        for repo_name, daily_stats in repo_stats.items():
            safe_repo_name = repo_name.replace('/', '_')

            # Export CSV summary
            daily_stats.to_csv(
                f"{self.output_dir}/{safe_repo_name}_daily_summary.csv",
                index=False
            )

            # Create readable report
            self._create_daily_report(repo_name, daily_stats)

    def _create_daily_report(self, repo_name: str, daily_stats: pd.DataFrame):
        """Create a readable daily report for a repository in Markdown format."""   # noqa
        safe_repo_name = repo_name.replace('/', '_')
        with open(f"{self.output_dir}/{safe_repo_name}_daily_report.md", 'w') as f:  # noqa
            # Header
            f.write(f"# Activity Report for {repo_name}\n\n")
            f.write(
                f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")  # noqa

            # Repository Summary
            f.write("## Repository Summary\n\n")
            total_commits = daily_stats['commits'].sum()
            total_minutes = daily_stats['activity_minutes'].sum()
            total_days = len(daily_stats)
            total_additions = daily_stats['additions'].sum()
            total_deletions = daily_stats['deletions'].sum()

            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Total Commits | {total_commits:,} |\n")
            f.write(f"| Total Activity Time | {total_minutes:,} minutes |\n")
            f.write(f"| Active Days | {total_days:,} |\n")
            f.write(f"| Lines Added | {total_additions:,} |\n")
            f.write(f"| Lines Deleted | {total_deletions:,} |\n\n")

            # Daily Activity
            f.write("## Daily Activity\n\n")

            for _, row in daily_stats.iterrows():
                # Date header
                f.write(f"### {row['date']}\n\n")

                # Stats table
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                f.write(f"| Commits | {row['commits']:,} |\n")
                f.write(f"| Lines Added | +{row['additions']:,} |\n")
                f.write(f"| Lines Deleted | -{row['deletions']:,} |\n")
                f.write(f"| Activity Time | {
                        row['activity_minutes']} minutes |\n\n")

                # AI Summary
                f.write("#### Changes Summary\n\n")
                f.write(f"{row['commit_summary']}\n\n")

                # Separator for readability
                f.write("---\n\n")

    def _create_overall_summary(self, repo_stats: Dict[str, pd.DataFrame]):
        """Create an overall summary report in Markdown format."""
        with open(f"{self.output_dir}/overall_summary.md", 'w') as f:
            # Header
            f.write("# Overall Activity Summary\n\n")
            f.write(
                f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")  # noqa

            # Summary table header
            f.write(
                "| Repository | Commits | Activity Time | Active Days | Lines Added | Lines Deleted |\n")  # noqa
            f.write(
                "|------------|---------|---------------|-------------|-------------|---------------|\n")   # noqa

            # Calculate totals
            total_commits = 0
            total_minutes = 0
            total_additions = 0
            total_deletions = 0

            for repo_name, daily_stats in repo_stats.items():
                commits = daily_stats['commits'].sum()
                minutes = daily_stats['activity_minutes'].sum()
                days = len(daily_stats)
                additions = daily_stats['additions'].sum()
                deletions = daily_stats['deletions'].sum()

                # Add to totals
                total_commits += commits
                total_minutes += minutes
                total_additions += additions
                total_deletions += deletions

                # Write repository row
                f.write(f"| {repo_name} | {commits:,} | {minutes:,} | {
                        days:,} | {additions:,} | {deletions:,} |\n")

            # Write totals row
            f.write(
                "|------------|---------|---------------|-------------|-------------|---------------|\n")  # noqa
            f.write(f"| **TOTAL** | **{total_commits:,}** | **{total_minutes:,}** | **-** | **{  # noqa
                    total_additions:,}** | **{total_deletions:,}** |\n\n")

            # Detailed Statistics Section
            f.write("## Detailed Repository Statistics\n\n")

            for repo_name, daily_stats in repo_stats.items():
                f.write(f"### {repo_name}\n\n")

                # Calculate repository metrics
                total_days = len(daily_stats)
                active_days_list = daily_stats.index.tolist()  # noqa
                avg_commits_per_day = daily_stats['commits'].mean()
                max_commits_day = daily_stats.loc[daily_stats['commits'].idxmax()]  # noqa

                # Write detailed stats
                f.write("#### Activity Metrics\n\n")
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                f.write(f"| Total Active Days | {total_days:,} |\n")
                f.write(f"| Average Commits per Day | {
                        avg_commits_per_day:.2f} |\n")
                f.write(f"| Most Active Day | {max_commits_day.name} ({
                        max_commits_day['commits']} commits) |\n")
                f.write("\n---\n\n")
