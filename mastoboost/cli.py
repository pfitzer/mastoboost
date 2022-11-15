import os
import platform
import sys
from getpass import getpass

import yaml

from mastoboost.listener import Listener

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mastodon import Mastodon, StreamListener
from mastoboost.options import options

CLIENT_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_clientcred.secret'))
USER_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_usercred.secret'))


def register_app():
    uri = input('Mastodon URL: ')
    login = input('login: ')
    if platform.system() in ['linux', 'linux2', 'darwin']:
        pw = getpass(prompt='Password: ')
    else:
        pw = input('Password: ')
    Mastodon.create_app(
        'feedTheMastodon',
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


class MastoBoot:

    mastodon = None

    def __init__(self):
        self.mastodon = Mastodon(access_token=USER_CRED)
        listener = Listener()
        toots = self.mastodon.stream_hashtag('mastodon', listener)
        print(toots)


if __name__ == '__main__':
    mb = MastoBoot()
