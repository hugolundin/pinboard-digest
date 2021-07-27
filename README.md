# Pinboard Digest

A script that will email a digest of Pinboard bookmarks that have been saved during a given time period.

All too often, I find myself saving bookmarks for later and then never reading them. With this script on a cronjob, I can give myself things to read at a more convenient time.

## Environment variables

The script expects a number of variables to be defined:

```text
PINBOARD_API_TOKEN=
PINBOARD_DIGEST_DAYS=2

PINBOARD_DIGEST_SMTP_FROM_NAME=Pinboard Digest
PINBOARD_DIGEST_SMTP_FROM_EMAIL=source@email.com
PINBOARD_DIGEST_SMTP_TO=destination@email.com
PINBOARD_DIGEST_SMTP_SERVER=
PINBOARD_DIGEST_SMTP_PORT=587
PINBOARD_DIGEST_SMTP_LOGIN=
PINBOARD_DIGEST_SMTP_PASSWORD=
```

They will be either be read from the environment or from a file called `.env`.

## Usage

The script is run with `python3 main.py`. No flags exist at the moment. 
