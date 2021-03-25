import re

from sanic import Sanic
from sanic.response import html
from data.show.link_data import LinkShower

app = Sanic(__name__)


@app.route('/link/<link_name:string>')
async def download_link(request, link_name):
    link = link_name.replace('_dot_', '.')
    link = re.match('[a-zA-z0-9_]+[.][a-z]+', link).group(0)
    LS = LinkShower(link)
    res = await LS.show_link_message_data()
    return html(res)


app.run()
