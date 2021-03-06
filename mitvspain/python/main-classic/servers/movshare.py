# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# MiTvSpain - XBMC Plugin
# Conector para Movshare

# ------------------------------------------------------------
# Credits:
# https://github.com/Eldorados/script.module.urlresolver/blob/master/lib/urlresolver/plugins/movshare.py

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if "This file no longer exists on our servers" in data:
        return False, "El fichero ha sido borrado de movshare"

    return True, ""


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    videoid = scrapertools.get_match(page_url, "http://www.movshare.net/video/([a-z0-9]+)")
    video_urls = []

    # Descarga la página
    headers = []
    headers.append(
        ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'])
    html = scrapertools.cache_page(page_url, headers=headers)

    # La vuelve a descargar, como si hubieras hecho click en el botón
    # html = scrapertools.cache_page(page_url , headers = headers)
    filekey = scrapertools.find_single_match(html, 'flashvars.filekey="([^"]+)"')

    # get stream url from api
    api = 'http://www.movshare.net/api/player.api.php?key=%s&file=%s' % (filekey, videoid)
    headers.append(['Referer', page_url])

    html = scrapertools.cache_page(api, headers=headers)
    logger.info("html=" + html)
    stream_url = scrapertools.find_single_match(html, 'url=(.+?)&title')

    if stream_url != "":
        video_urls.append([scrapertools.get_filename_from_url(stream_url)[-4:] + " [movshare]", stream_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.movshare.net/video/deg0ofnrnm8nq
    patronvideos = 'movshare.net/video/([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'movshare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    #
    patronvideos = "movshare.net/embed/([a-z0-9]+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'movshare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://embed.movshare.net/embed.php?v=xepscujccuor7&width=1000&height=450
    patronvideos = "movshare.net/embed.php\?v\=([a-z0-9]+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'movshare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
