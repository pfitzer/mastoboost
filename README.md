# mastoboost
## A bot for boosting Mastodon toots with given hashtags.

### get the code
If you want to run the code without docker

```bash
# clone the repository
git clone https://github.com/pfitzer/mastoboost.git
cd mastoboost
# create virtualenv
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt

# authorize the app on your Mastodon instance
python mastoboost/cli.py -r
# and follow the cli
# Mastodon URL:
# username:
# password:

# create a cronjob
*/5 * * * * cd /path/to/mastoboost && env/bin/activate && /path/to/python mastodon/cli.py >> cron_log.log 2>&1
```


### config
The hashtags are defined in the config.yml file.

```
# config.yml
hashtags:
- tag1
- tag2
- tag3
```

### run with docker

```bash
docker pull pfitzer/mastoboost:latest

# authoríze the app on your Mastodon instance
docker run -i pfitzer/mastoboost:latest /usr/local/bin/python mastoboost/cli.py -r
# run the container
docker run -d --mount type=bind,source="/absolute/path/to/config.yml",target=/app/config.yml pfitzer/mastoboost:latest
```