import argparse
import logging
import os
import sys
from pathlib import Path

from mattermostdriver import Driver


def post(markdown_file: Path, channel: str = 'APD'):
    mattermost = Driver({
        'url': 'chat.asf.alaska.edu',
        'token': os.environ.get('MATTERMOST_PAT'),
        'scheme': 'https',
        'port': 443
    })
    response = mattermost.login()
    logging.debug(response)

    channel_info = mattermost.channels.get_channel_by_name_and_team_name('asf', channel)

    markdown = markdown_file.read_text()
    response = mattermost.posts.create_post(
        options={
            'channel_id': channel_info['id'],
            'message': markdown,
        }
    )
    logging.debug(response)

    return response


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('markdown_file', type=Path, help='Markdown file with the post content')
    parser.add_argument('--channel', default='tools-team', help='The MatterMost channel to post to')

    args = parser.parse_args()

    out = logging.StreamHandler(stream=sys.stdout)
    out.addFilter(lambda record: record.levelno <= logging.INFO)
    err = logging.StreamHandler()
    err.setLevel(logging.WARNING)
    logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=(out, err))

    post(**args.__dict__)
