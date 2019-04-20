from feedgen.feed import FeedGenerator
from os import listdir, rename
from os.path import isfile, join, getsize
from s3upload import upload_file

fg = FeedGenerator()
fg.load_extension('podcast')
fg.id('http://dannyshaw.github.io/podcast-feeds')
fg.title('Danny\'s Podcasts')
fg.author({'name': 'Danny Shaw', 'email': 'code@dannyshaw.io'})
fg.link(href='http://dannyshaw.github.io/podcast-feeds', rel='alternate')
fg.subtitle('My personal rss feed...')
fg.link(href='http://dannyshaw.github.io/podcast-feeds/rss.xml', rel='self')
fg.language('en')

FILES = '/home/danny/Downloads/audio'

episodes = sorted([f for f in listdir(FILES) if isfile(join(FILES, f))])

for ep in episodes:
    # upload_file(join(FILES, ep), 'danny.podcasts.seinfeld', ep)
    file_size = getsize(join(FILES, ep))
    fe = fg.add_entry()
    fe.id(f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}')
    fe.title(ep)
    fe.link(href=f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}')
    fe.enclosure(f'https://s3.amazonaws.com/danny.podcasts.seinfeld/{ep}',
                 f'{file_size}', 'audio/mpeg')

# ep.rename()
# Write the RSS feed to a file
fg.rss_str(pretty=True)
fg.rss_file('rss.xml')


def rename_files():
    FILES = '/home/danny/Downloads/audio'
    episodes = [f for f in listdir(FILES) if isfile(join(FILES, f))]
    for ep in episodes:
        file_name = join(FILES, ep)
        new_name = (ep.replace(' - ', '-').replace(' ', '-').replace('(', '')
                    .replace(')', '').replace(',-', '-').lower())
        rename(file_name, join(FILES, new_name))
