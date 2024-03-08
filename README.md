# mastoboost
## A bot for boosting Mastodon toots with given hashtags.

[![Create Release](https://github.com/pfitzer/mastoboost/actions/workflows/build.yaml/badge.svg)](https://github.com/pfitzer/mastoboost/actions/workflows/build.yaml)

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

# create envorionment variables
export INSTANCE=https://...
export USERNAME=YOUR_USERNAME
export PASSWORD=YOUR_PASSWORD

nohup python mastoboost/cli.py > /path/to/output.log 2>&1 &
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

### run with docker compose

```bash
cp config-sample.yml config.yml
cp .env.example .env
# and edit them matching your needs
```

```yaml
version: '3'

services:
  app:
    image: pfitzer/mastoboost
    volumes:
      - ./config.yml:/app/config.yml
    env_file:
      - .env
    environment:
      - PYTHONUNBUFFERED=1
    command: >
      sh -c "python mastoboost/cli.py"
```