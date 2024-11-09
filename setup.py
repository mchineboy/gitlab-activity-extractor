
# File: setup.py
from setuptools import setup, find_packages

setup(
    name="gitlab-activity-extractor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'openai>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'gitlab-activity=src.main:main',
        ],
    },
    python_requires='>=3.8',
    author="Tyler Hardison",
    author_email="tyler@seraphnet.com",
    description="A tool to extract and analyze GitLab commit activity",
    keywords="gitlab,git,activity,commits,analysis",
)
