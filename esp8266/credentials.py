class Credentials:
    """
    This class holds all secrets used in this project.
    After change beware of accidentally committing this to git run the following command:
        `git update-index --skip-worktree esp8266/credentials.py`

    If a change is needed, when for instance credentials are added, run the following command:
        `git update-index --no-skip-worktree esp8266/credentials.py`
    Save your edits and revert the changes to the latest HEAD:
        `git checkout HEAD -- esp8266/credentials.py`
    Add stuff that is devoid of any secrets, and lock the file again.
        `git update-index --skip-worktree esp8266/credentials.py`
    Now restate the secrets you added and add the new ones.
    """
    SSID = "[[wifi network name]]"
    PASSWORD = "[[wifi network pass]]"
