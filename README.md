# 🕵️‍♂️ GitLab Activity Extractor 

_Because sometimes you need to prove you've been working hard, not hardly working._

## 📋 Overview

GitLab Activity Extractor is a powerful tool that analyzes your GitLab commit history and generates detailed reports about your coding activity. Whether you're tracking project progress, preparing for performance reviews, or just curious about your work patterns, this tool has got you covered.

## ✨ Features

- 🗂️ **Repository-Level Analysis**: Break down activity by repository (because not all repos are created equal)
- 📊 **Detailed Statistics**: Track additions, deletions, and time spent (warning: numbers may induce existential crisis)
- 🤖 **AI-Powered Summaries**: Uses OpenAI to summarize commit messages (so you don't have to relive your "fixed typo" commits)
- 📅 **Daily Activity Reports**: Beautiful Markdown reports that make your Git activity look professional (even if half the commits are "WIP")
- 📈 **Aggregate Statistics**: Total time spent, lines changed, and more (perfect for justifying your coffee budget)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gitlab-activity-extractor.git

# Install the package
cd gitlab-activity-extractor
pip install -e .

# Celebrate your successful installation
echo "🎉 Ready to stalk your own Git history!"
```

## 🔧 Configuration

You'll need a few things to get started:

1. A GitLab personal access token (with `read_api` scope)
2. Your GitLab group ID
3. (Optional) An OpenAI API key for commit summaries
4. (Optional) A good excuse for all those "minor fixes" commits

## 🎮 Usage

### Basic Usage

```bash
gitlab-activity --token glpat-xxxx --group-id 12345
```

### Advanced Usage (For Overachievers)

```bash
gitlab-activity \
    --token glpat-xxxx \
    --group-id 12345 \
    --gitlab-url https://gitlab.example.com \
    --author-email your.name@company.com \
    --minutes-per-commit 20 \
    --output-prefix productivity_proof \
    --start-date 2024-01-01 \
    --openai-key sk-xxxx \
    --debug
```

### Environment Variables (For the Security Conscious)

```bash
export GITLAB_TOKEN=glpat-xxxx
export GITLAB_GROUP_ID=12345
export OPENAI_API_KEY=sk-xxxx
gitlab-activity
```

## 📝 Command Line Arguments

| Argument | Environment Variable | Description |
|----------|---------------------|-------------|
| `--token` | `GITLAB_TOKEN` | Your GitLab API token (required, unless you're a wizard) |
| `--group-id` | `GITLAB_GROUP_ID` | Group ID to analyze (required) |
| `--gitlab-url` | `GITLAB_URL` | GitLab instance URL (default: [https://gitlab.com](https://gitlab.com)) |
| `--author-email` | `GITLAB_AUTHOR_EMAIL` | Filter by author (in case you're only interested in your own mistakes) |
| `--minutes-per-commit` | `MINUTES_PER_COMMIT` | Estimated time per commit (default: 15, adjust for procrastination level) |
| `--start-date` | `START_DATE` | Start date (YYYY-MM-DD) |
| `--output-prefix` | `OUTPUT_PREFIX` | Prefix for output files |
| `--openai-key` | `OPENAI_API_KEY` | OpenAI API key (for fancy commit summaries) |
| `--debug` | `DEBUG` | Enable debug output (for when things go wrong) |

## 📊 Output Files

The tool generates several files in a `{output_prefix}_by_repo` directory:

- `{repo}_detailed.csv`: Every. Single. Commit. (The raw truth)
- `{repo}_daily_summary.csv`: Daily stats (for the spreadsheet enthusiasts)
- `{repo}_daily_report.md`: Pretty Markdown report (perfect for showing your boss)
- `overall_summary.md`: The big picture (spoiler: you wrote a lot of code)

## 🤓 For Developers

Want to contribute? Great! Here's how:

1. Fork the repository
2. Create your feature branch
3. Write some amazing code
4. Submit a pull request
5. Wait patiently while we analyze your commit history 😉

## 🐛 Troubleshooting

1. **Q: Why aren't my commits showing up?**  
   A: Check your token permissions. Or maybe you haven't committed anything (it happens to the best of us).

2. **Q: The time calculations seem off.**  
   A: Adjust `--minutes-per-commit`. We know you're not really that fast.

3. **Q: The AI summaries are weird.**  
   A: That's not a bug, that's OpenAI trying to make sense of your commit messages.

## 📜 License

MIT License (because sharing is caring)

## 🙏 Acknowledgments

- Coffee ☕
- Stack Overflow 🚀
- That one person who actually writes good commit messages 🏆

## 💡 Final Note

Remember: Git activity is not a perfect measure of productivity. Sometimes the best code is the code you delete!

---

_Made with 💖 and probably too much caffeine._

```python
if __name__ == "__main__":
    print("Now go forth and analyze!")
```
