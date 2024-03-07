import os
import platform
import sys
import re
from getpass import getpass

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mastodon import Mastodon, StreamListener
from options import options

CLIENT_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_clientcred.secret'))
USER_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_usercred.secret'))
CONFIG = os.path.join(os.path.dirname(__file__), '..', 'config.yml')


def register_app():
    """
    register the app on a Mastodon instance
    :return:
    """
    regex = r"(%0d|=)"
    uri = input('Mastodon URL: ')
    uri = re.sub(regex, '', uri, 0, re.MULTILINE)
    login = input('login: ')
    if platform.system() in ['linux', 'linux2', 'darwin']:
        pw = getpass(prompt='Password: ')
    else:
        pw = input('Password: ')
    Mastodon.create_app(
        'MastoBoost',
        api_base_url=uri,
        to_file=CLIENT_CRED
    )
    mastodon = Mastodon(
        client_id=CLIENT_CRED,
        api_base_url=uri
    )

    mastodon.log_in(
        login,
        pw,
        to_file=USER_CRED,
    )


class Listener(StreamListener):

    def __init__(self):
        with open(CONFIG, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=Loader)

    def on_update(self, status):
        if status["visibility"] in ("public", "unlisted"):
            content = status["content"]
            print(f"processing {status['id']}")
            for hashtag in self.config["hashtags"]:
                if f"#{hashtag}" in content:
                    print(f"Boosting status {status['id']}")
                    mastodon.status_reblog(status["id"])
                    break


if options.register or not os.path.exists(USER_CRED) or not os.path.exists(CLIENT_CRED):
    register_app()
    sys.exit(0)

if options.listen:
    mastodon = Mastodon(
        access_token='ftm_usercred.secret',
        api_base_url='https://social.main-angler.de'
    )

    listener = Listener()
    mastodon.stream_public(listener)
