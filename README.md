## Auto Jira smart commit

This [pre-commit](https://pre-commit.com/) hook transforms your Git commit messages into [Jira smart commits](https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html).

If your branch name contains a [Jira issue key](https://confluence.atlassian.com/adminjiraserver073/changing-the-project-key-format-861253229.html) such as `ABC-123`, the hook will automatically format your commit message into a Jira smart commit:

| Command | Log entry |
| ------- | --------- |
| git commit -m "release the kraken." | ABC-123 Release the kraken<br><br>ABC-123 #time 0w 0d 2h 8m Release the kraken<br><br>_Effect:_ Logs the time since your last commit on any branch in the Work Log tab. |
| git commit -m "Release the kraken<br><br>A kraken lives in dark depths, usually a sunken rift or a cavern filled with detritus, treasure, and wrecked ships." | ABC-123 Release the kraken<br><br>ABC-123 #comment A kraken lives in dark depths, usually a sunken rift or a cavern filled with detritus, treasure, and wrecked ships.<br><br>ABC-123 #time 0w 0d 2h 8m Release the kraken<br><br>_Effect:_ Posts a comment to the Jira issue and logs the time since your last commit in the Work Log tab. |

If the branch name does not contain a Jira issue key, the commit message is not modified. The time logged takes into account non-working hours such as lunch breaks and nights.

See [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/) for an explanation of the seven rules of a great Git commit message:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line (automated)
4. Do not end the subject line with a period (automated)
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

## Installation

Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/radix-ai/auto-smart-commit
    rev: v1.0.1
    hooks:
      - id: auto-smart-commit
```
