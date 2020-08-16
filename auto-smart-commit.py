#!/usr/bin/env python

import re
import sys
from datetime import datetime
from math import floor
from subprocess import check_output
from typing import NoReturn, Optional


def run_command(command: str) -> str:
    try:
        stdout: str = check_output(command.split()).decode("utf-8").strip()
    except Exception:
        stdout = ""
    return stdout


def current_git_branch_name() -> str:
    return run_command("git symbolic-ref --short HEAD")


def extract_jira_issue_key(message: str) -> Optional[str]:
    project_key, issue_number = r"[A-Z]{2,}", r"[0-9]+"
    match = re.search(f"{project_key}-{issue_number}", message)
    if match:
        return match.group(0)
    return None


def last_commit_datetime() -> datetime:
    # https://git-scm.com/docs/git-log#_pretty_formats
    git_log = "git log -1 --branches --format=%aI"
    author = run_command("git config user.email")
    last_author_datetime = run_command(f"{git_log} --author={author}") or run_command(git_log)
    if "+" in last_author_datetime:
        return datetime.strptime(last_author_datetime.split("+")[0], "%Y-%m-%dT%H:%M:%S")
    return datetime.now()


def num_lunches(start: datetime, end: datetime) -> int:
    n = (end.date() - start.date()).days - 1
    if start < start.replace(hour=12, minute=0, second=0):
        n += 1
    if end > end.replace(hour=12, minute=45, second=0):
        n += 1
    return max(n, 0)


def num_nights(start: datetime, end: datetime) -> int:
    n = (end.date() - start.date()).days - 1
    if start < start.replace(hour=1, minute=0, second=0):
        n += 1
    if end > end.replace(hour=5, minute=0, second=0):
        n += 1
    return max(n, 0)


def time_worked_on_commit() -> Optional[str]:
    now = datetime.now()
    last = last_commit_datetime()
    # Determine the number of minutes worked on this commit as the number of
    # minutes since the last commit minus the lunch breaks and nights.
    working_hours_per_day = 8
    working_days_per_week = 5
    minutes = max(
        round((now - last).total_seconds() / 60)
        - num_nights(last, now) * (24 - working_hours_per_day) * 60
        - num_lunches(last, now) * 45,
        0,
    )
    # Convert the number of minutes worked to working weeks, days, hours,
    # minutes.
    if minutes > 0:
        hours = floor(minutes / 60)
        minutes -= hours * 60
        days = floor(hours / working_hours_per_day)
        hours -= days * working_hours_per_day
        weeks = floor(days / working_days_per_week)
        days -= weeks * working_days_per_week
        return f"{weeks}w {days}d {hours}h {minutes}m"
    return None


def main() -> NoReturn:
    # https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html
    # Exit if the branch name does not contain a Jira issue key.
    git_branch_name = current_git_branch_name()
    jira_issue_key = extract_jira_issue_key(git_branch_name)
    if not jira_issue_key:
        sys.exit(0)
    # Read the commit message.
    commit_msg_filepath = sys.argv[1]
    with open(commit_msg_filepath, "r") as f:
        commit_msg = f.read()
    # Split the commit into a subject and body and apply some light formatting.
    commit_elements = commit_msg.split("\n", maxsplit=1)
    commit_subject = commit_elements[0].strip()
    commit_subject = f"{commit_subject[:1].upper()}{commit_subject[1:]}"
    commit_subject = re.sub(r"\.+$", "", commit_subject)
    commit_body = None if len(commit_elements) == 1 else commit_elements[1].strip()
    # Build the new commit message:
    # 1. If there is a body, turn it into a comment on the issue.
    if "#comment" not in commit_msg and commit_body:
        commit_body = f"{jira_issue_key} #comment {commit_body}"
    # 2. Add the time worked to the Work Log in the commit body.
    work_time = time_worked_on_commit()
    if "#time" not in commit_msg and work_time:
        work_log = f"{jira_issue_key} #time {work_time} {commit_subject}"
        commit_body = f"{commit_body}\n\n{work_log}" if commit_body else work_log
    # 3. Make sure the subject starts with a Jira issue key.
    if not extract_jira_issue_key(commit_subject):
        commit_subject = f"{jira_issue_key} {commit_subject}"
    # Override commit message.
    commit_msg = f"{commit_subject}\n\n{commit_body}" if commit_body else commit_subject
    with open(commit_msg_filepath, "w") as f:
        f.write(commit_msg)
    sys.exit(0)


if __name__ == "__main__":
    main()
