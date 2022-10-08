import argparse
import logging
import os
import sys
from pathlib import Path
from pprint import pprint
from typing import Tuple, Union

import boto3
import mistune
from premailer import transform

from bullets.util import render_template

SES = boto3.client('ses', os.environ.get('AWS_REGION', os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')))


def content(markdown_file: Path) -> Tuple[str, str]:
    markdown = markdown_file.read_text()

    markdown2html = mistune.Markdown()
    html = markdown2html(markdown)
    # attach style and headers
    html = render_template('email.j2', content=html)
    # move style inline
    html = transform(html, pretty_print=True)

    return html, markdown


def send(sender: str, to: Union[str, list], subject: str, html: str, text: str) -> dict:
    if isinstance(to, str):
        to = [to]

    return SES.send_email(
        Source=sender,
        Destination={'ToAddresses': to},
        Message={
            'Body': {
                'Html': {'Data': html, 'Charset': 'utf-8'},
                'Text': {'Data': text, 'Charset': 'utf-8'},
            },
            'Subject': {'Data': subject, 'Charset': 'utf-8'}
        }
    )


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('markdown_file', type=Path, help='Markdown file with the email content')
    parser.add_argument('sender', help='Send email from this address')
    parser.add_argument('subject', help='Subject of the email')
    parser.add_argument('to', nargs='+', help='Send email to these addresses')

    args = parser.parse_args()

    out = logging.StreamHandler(stream=sys.stdout)
    out.addFilter(lambda record: record.levelno <= logging.INFO)
    err = logging.StreamHandler()
    err.setLevel(logging.WARNING)
    logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=(out, err))

    html, text = content(markdown_file=args.markdown_file)
    response = send(sender=args.sender, to=args.to, subject=args.subject, html=html, text=text)
    pprint(response)
