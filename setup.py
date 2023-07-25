from setuptools import setup

setup(
    name="auto-smart-commit",
    version="1.0.3",
    py_modules=["auto_smart_commit"],
    entry_points={
        "console_scripts": [
            "auto-smart-commit=auto_smart_commit:main",
        ],
    },
    author="Laurent Sorber",
    author_email="laurent@radix.ai",
    description="Automatically transform your Git commit messages into Jira smart commits",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
