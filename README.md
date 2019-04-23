## Automated Jira smart commits

This [`prepare-commit-msg`](https://git-scm.com/docs/githooks#_prepare_commit_msg) Git hook transforms your Git commit messages into [Jira smart commits](https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html).

After naming your branch after a [Jira issue key](https://confluence.atlassian.com/adminjiraserver073/changing-the-project-key-format-861253229.html) such as `ML-42`, the hook will automatically format your commit message into a Jira smart commit:

| Command | Log entry |
| ------- | --------- |
| ``git commit -m "open the pod bay doors."`` | ``ML-42 Open the pod bay doors``<br><br>``Jira #time 0w 0d 2h 8m Open the pod bay doors``<br><br>_Effect:_ Logs the time since your last commit on any branch in the Work Log tab. |
| ``git commit -m "Open the pod bay doors``<br><br>``I should get back inside, so I must open the pod bay doors."`` | ``ML-42 Open the pod bay doors``<br><br>``Jira #comment I should get back inside, so I must open the pod bay doors.``<br><br>``Jira #time 0w 0d 2h 8m Open the pod bay doors``<br><br>_Effect:_ Posts a comment to the Jira issue and logs the time since your last commit in the Work Log tab. |
| ``git commit`` | ``ML-42 d$:<If applied, this commit will "Open the pod bay doors">``<br><br>``Jira #comment d$:<What does this commit do, and why?>``<br><br>``Jira #time 0w 0d 2h 8m Open the pod bay doors``<br><br>_Effect:_ Edit the smart commit with your favourite editor before publishing it.<br><br>Since the default is usually Vim, we remind the user how to delete a line starting from the cursor with `d$`. |

See [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/) for an explanation of the seven rules of a great Git commit message:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

## Installation

To install the git hooks in the directory `githooks`, run the following command from the root of your repository:
```bash
git config --local core.hooksPath githooks
```
