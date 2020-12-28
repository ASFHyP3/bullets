import jinja2


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
