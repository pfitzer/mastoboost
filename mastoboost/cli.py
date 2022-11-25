import os
import platform
import sys
import re
import time
from datetime import datetime
from getpass import getpass

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mastodon import Mastodon
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


if options.register or not os.path.exists(USER_CRED) or not os.path.exists(CLIENT_CRED):
    register_app()
    sys.exit(0)


class MastoBoost(object):
    """
    all the logic is here
    """
    def __init__(self):
        self.mastodon = Mastodon(access_token=USER_CRED)
        self.__load_settings()
        tooted = []
        last = datetime.fromtimestamp(self.settings['last_id']) if 'last_id' in self.settings else None
        for tag in self.settings['hashtags']:
            toots = self.mastodon.timeline(timeline=f'tag/{tag}', since_id=last, remote=True, limit=None)

            for toot in toots:
                if toot['id'] not in tooted:
                    print("boosted toot: {id}".format(id=toot['id']))
                    #self.mastodon.status_reblog(toot['id'])
                tooted.append(toot['id'])

        self.__update_settings()

    def __load_settings(self):
        """
        load the settings from config.yml
        :return:
        """
        try:
            f = open(CONFIG)
        except FileNotFoundError:
            raise Exception(f'{CONFIG} not found')
        self.settings = yaml.load(f, Loader=Loader)

    def __update_settings(self):
        """
        wright the last processed toot id to config.yml
        :param last_id:
        :return:
        """
        self.settings['last_id'] = int(time.time())
        yaml.dump(self.settings, open(CONFIG, 'w'), Dumper=Dumper)


if __name__ == '__main__':
    mb = MastoBoost()
