# File: src/ai_summarizer.py
from typing import List
from openai import OpenAI


class CommitSummarizer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.assistant = self._create_assistant()

    def _create_assistant(self):
        """Create an OpenAI assistant for commit summarization."""
        models = self.client.models.list()
        print("Available models:")
        for model in models:
            print(f"- {model.id}")
        print("\nUsing default model: gpt-4o")

        return self.client.beta.assistants.create(
            name="Git Commit Summarizer",
            description="Summarize git commit messages",
            model="gpt-4o",
            instructions="Please summarize these git commits, focusing on the main themes and important changes. Be concise but informative. Commits might not be very wordy. Note that this is an application that deals with reconveyance for real estate, try to extract meanings with this additional information."  # noqa
        )

    def summarize_commits(self, commit_messages: List[str]) -> str:
        """Use AI to summarize a list of commit messages."""
        if not commit_messages:
            return "No commits to summarize"

        try:
            thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=" ".join(commit_messages)
            )

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=self.assistant.id,
                instructions="Please summarize these git commits, focusing on the main themes and important changes. Be concise but informative."  # noqa
            )

            print("Run completed with status: " + run.status)

            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id)
                summary = ""
                for message in messages:
                    assert message.content[0].type == "text"
                    summary += message.content[0].text.value + " "
                return summary
            else:
                print(f"Error generating AI summary: {run}")
                return "Error generating summary"
        except Exception as e:
            print(f"Error generating AI summary: {str(e)}")
            return "Error generating summary"

    def cleanup(self):
        """Clean up AI resources."""
        try:
            self.client.beta.assistants.delete(self.assistant.id)
        except Exception as e:
            print(f"Error cleaning up AI assistant: {str(e)}")
