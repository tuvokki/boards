class Credentials:
    """
    This class holds all secrets used in this project.
    After change beware of accidentally committing this to git run the following command:
        `git update-index --skip-worktree esp32/credentials.py`

    If a change is needed, when for instance credentials are added, run the following command:
        `git update-index --no-skip-worktree esp32/credentials.py`

    """
    SSID = "[[wifi network name]]"
    PASSWORD = "[[wifi network pass]]"
