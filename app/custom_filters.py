import re

from jinja2 import pass_eval_context
from markupsafe import Markup, escape

from app import app


@pass_eval_context
def linebreaksbr(eval_ctx, value):
    br = "<br>\n"

    if eval_ctx.autoescape:
        value = escape(value)
        br = Markup(br)

    result = "\n\n".join(
        f"<p>{br.join(p.splitlines())}"
        for p in re.split(r"(?:\r\n|\r(?!\n)|\n){2,}", value)
    )
    return Markup(result) if eval_ctx.autoescape else result


app.jinja_env.filters['linebreaksbr'] = linebreaksbr
