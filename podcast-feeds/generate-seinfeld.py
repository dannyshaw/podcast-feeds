from feedgen.feed import FeedGenerator
from os import listdir, rename
from os.path import isfile, join, getsize
from s3upload import upload_file
from datetime import datetime, timezone, timedelta

FILES = '/home/danny/Downloads/audio'


def generate_feed_from_episodes(episodes):
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id('http://dannyshaw.github.io/podcast-feeds')
    fg.title('Seinfeld Complete Audio')
    fg.link(href='http://dannyshaw.github.io/podcast-feeds', rel='alternate')
    fg.subtitle('I\'ve seen them enough, audio is all I need.')
    fg.link(
        href='http://dannyshaw.github.io/podcast-feeds/rss.xml', rel='self')
    fg.language('en')

    for index, ep in enumerate(episodes):
        file_size = getsize(join(FILES, ep))
        fe = fg.add_entry()
        fe.id(f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}')
        fe.title(ep)
        fe.description(ep)

        pub_date = datetime(1999, 1, 1, tzinfo=timezone.utc) + timedelta(index)

        fe.pubDate(pub_date)
        fe.link(href=f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}')
        fe.enclosure(f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}',
                     f'{file_size}', 'audio/mpeg')

    fg.rss_str(pretty=True)
    fg.rss_file('rss.xml')


def upload_to_s3(episodes):
    for index, ep in enumerate(episodes):
        upload_file(join(FILES, ep), 'danny.podcasts.seinfeld', ep)


def rename_files():
    FILES = '/home/danny/Downloads/audio'
    episodes = [f for f in listdir(FILES) if isfile(join(FILES, f))]
    for ep in episodes:
        file_name = join(FILES, ep)
        new_name = (ep.replace(' - ', '-').replace(' ', '-').replace('(', '')
                    .replace(')', '').replace(',-', '-').lower())
        rename(file_name, join(FILES, new_name))


episodes = sorted([f for f in listdir(FILES) if isfile(join(FILES, f))])
# upload_to_s3(episodes)
generate_feed_from_episodes(episodes)
