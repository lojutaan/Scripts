# pocket.py
This script sends the saved urls from [Pocket](https://getpocket.com/) to [ArchiveBox](https://archivebox.io/) running in Docker container for archival. This script is meant to be run periodically with cron. 

## Example cron
This will run the script every hour between 7AM and 10PM
```
0 7-22 * * * /usr/bin/python3 /Scripts/pocket2archivebox/pocket.py
```