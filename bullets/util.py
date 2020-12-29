from dateutil.parser import parse as parse_date
from fastcore.basics import AttrDict
from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape


def get_environment() -> Environment:
    env = Environment(
        loader=PackageLoader('bullets', 'templates'),
        autoescape=select_autoescape(['html.j2']),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    return env


def render_template(template: str, **kwargs) -> str:
    env = get_environment()
    template = env.get_template(template)
    rendered = template.render(**kwargs)
    return rendered


def get_details(node: AttrDict) -> dict:
    name = node.get('name')
    if name is None:
        repo = '/'.join(node.html_url.split('/')[-4:-2])
        name = f'{repo} #{node.number}'

    created_at = parse_date(node.created_at)
    return {
        'name': name,
        'title': node.get('title', ''),
        'body': node.body,
        'html_url': node.html_url,
        'created_at': created_at,
    }

