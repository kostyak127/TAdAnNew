import pytest

from data.messages.download.messages import MessageDownloader


def test_find_channels_from_message_text():
    assert MessageDownloader.find_channels_from_message_text('@channel_1 sdasd https://t.me/channel_smth https://t.me/joinchat/AAAAAE5vilx2u8frc8oKAw') \
           == ['t.me/channel_smth', 't.me/joinchat/AAAAAE5vilx2u8frc8oKAw', 'channel_1']


def test_find_links_from_message_text():
    assert MessageDownloader.find_links_from_message_text('https://t.me/smth asdasd youtube.com www.smth.ru')\
           == ['youtube.com', 'smth.ru']
