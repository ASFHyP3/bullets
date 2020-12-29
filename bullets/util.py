import jinja2
from dateutil.parser import parse as parse_date
from fastcore.basics import AttrDict


def get_environment() -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('bullets', 'templates'),
        autoescape=jinja2.select_autoescape(['html.j2']),
        undefined=jinja2.StrictUndefined,
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

