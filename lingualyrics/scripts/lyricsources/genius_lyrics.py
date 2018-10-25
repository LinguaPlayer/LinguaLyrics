#!/usr/bin/env python
from googlesearch import search as google_search
from requests import get
from bs4 import BeautifulSoup
import sys

def search(query):
    google_response = google_search(query + ' site:genius.com', stop=1)
    links = []
    for url in google_response:
            links.append(url)

    links_of_lyric_pages = []

    for link in links:
        # Remove url of other pages of genius.com
        if link.count('/') != 3:
            continue
        if link.split('/')[3] in ['artists-index', 'discussions']:  
            continue
        if (link.split('/')[3]).split('?')[0] in ['songs']:
            continue
        if link.count('-') == 0:
            continue
        if 'lyrics' not in link:
            continue
        else:
            links_of_lyric_pages.append(link)

    # list_of_links_with_description = [{'description': "",
    #                                    'url': "",
    #                                    'user_query': ""}]
    list_of_links_with_description = []
    for link in links_of_lyric_pages:
        url_lyric_description_part = link.split('/')[-1]
        # remove '-' and 'lyrics' word
        description = ' '.join(url_lyric_description_part.split('-')[:-1])
        list_of_links_with_description.append({'description': description,
                                               'url': link,
                                               'query': query})
    return list_of_links_with_description


def get_music_data(url):
    page = get(url)
    html = BeautifulSoup(page.text, "html.parser")
    # Scrape the song lyrics from the HTML
    lyrics_div = html.find("div", class_="lyrics")
    cover_art_img_tag = html.find("img", class_="cover_art-image")
    cover_art_image_url = cover_art_img_tag['src'] if cover_art_img_tag else None
    title_h1_tag = html.find("h1", class_="header_with_cover_art-primary_info-title")
    title = title_h1_tag.text if title_h1_tag else None
    artist_a_tag = html.find("a", class_="header_with_cover_art-primary_info-primary_artist")
    artist = artist_a_tag.text if artist_a_tag else None
    album_span_tag = html.find("span", class_="metadata_unit-info")
    album = album_span_tag.find('a').text if album_span_tag else None

    lyric_text = None
    if lyrics_div:
        lyric_text = (lyrics_div.get_text()).replace('\n\n', '')

    return {
        'success': lyric_text is not None,
        'url': url,
        'source': "genius.com",
        'lyric_text': lyric_text,
        'cover_art_image_url': cover_art_image_url,
        'artist': artist,
        'title': title,
        'album': album
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        links = search(query)
        correct_links = []
        print(get_music_data(links[0]['url'])['lyric_text'])
