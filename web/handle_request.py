import re

from sanic import Sanic
from sanic.request import Request
from sanic.response import html, json

from web.database import Database

db = Database()
app = Sanic(__name__)


@app.route('/link/<link_name:string>')
async def download_link(request: Request, link_name):
    link = link_name.replace('_dot_', '.')
    link = re.match('[a-zA-z0-9_]+[.][a-z]+', link).group(0)
    res = await show_link_message_data(db, link.replace('.', '_dot_'))
    return html(res)


async def show_link_message_data(db, link):
    html_ = """<head>
    <meta charset="utf-8">
    <link href="//telegram.org/css/widget-frame.css?45" rel="stylesheet" media="screen">
    <link href="//telegram.org/css/telegram-web.css?18" rel="stylesheet" media="screen">
    <script>TBaseUrl='/';</script>
  </head>
"""
    for message in await db.get_link_message_data(link):
        data = message[0]
        html_ += f"""<div class="tgme_widget_message_bubble"><div class="tgme_widget_message_author 
                accent_color"><a><span dir="auto">{message[1]}</span></a></div><i 
                class="tgme_widget_message_bubble_tail"> 
      <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
        <g fill="none">
          <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
          <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
          <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
          <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
        </g>
      </svg>
    </i> 
                <div class="tgme_widget_message_text js-message_text before_footer" dir="auto">{data['text_message']}
                </div>

<div class="tgme_widget_message_footer compact js-message_footer">

  <div class="tgme_widget_message_info short js-message_info">
    <span class="tgme_widget_message_views">{data['views']}</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"></span>
  </div>
</div>
  </div>
  <p></p>"""
    return html_


@app.route('/channel/<channel_name:string>')
async def download_channel(request, channel_name):
    res = await db.get_messages_data(channel_name)

    html_ = """<head>
        <meta charset="utf-8">

        <link href="//telegram.org/css/widget-frame.css?45" rel="stylesheet" media="screen">
        <link href="//telegram.org/css/telegram-web.css?18" rel="stylesheet" media="screen">
        <script>TBaseUrl='/';</script>
      </head>
    """
    for data in res:
        html_ += f"""<div class="tgme_widget_message_bubble"><div class="tgme_widget_message_author 
                accent_color"><a><span dir="auto">{"@" + channel_name} <b>упоминание: {data["mention"]}</b></span></a></div><i 
                class="tgme_widget_message_bubble_tail"> 
      <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
        <g fill="none">
          <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
          <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
          <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
          <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
        </g>
      </svg>
    </i> 
                <div class="tgme_widget_message_text js-message_text before_footer" dir="auto">{data['text_message']}
                </div>

<div class="tgme_widget_message_footer compact js-message_footer">

  <div class="tgme_widget_message_info short js-message_info">
    <span class="tgme_widget_message_views">{data['views']}</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"></span>
  </div>
</div>
  </div>
  <p></p>"""
    return html(html_)


@app.route('/connect_to_db', ['POST'])
async def connect_to_db(request: Request):
    if dict(request.json)['password'] == 'my_passworD':
        await db.create_connect()
        return json({"success": True})
    else:
        return json(body={"success": False}, status=403)
