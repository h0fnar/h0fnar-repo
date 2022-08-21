# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import requests
import json
import time

channel = sys.argv[1]
channel_id = sys.argv[2]

channel = "[COLOR darkorchid][B]" + channel + "[/B][/COLOR]"


_scriptid_ = "plugin.video.1spot.media"
_addon_ = xbmcaddon.Addon(id=_scriptid_)

_scriptname_ = _addon_.getAddonInfo('name')
_icon_ = _addon_.getAddonInfo('icon')

#################################################################


def get_epg(channel_id):
    main = ("https://www.1spotmedia.com/index.php/api/epg/get_epg_timeline_by_id?id=")
    link = main + channel_id
    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)

    max_guesses = le - 1
    i = 0
    epg = []

    while i <= max_guesses:

        show = parsed_json[i]['program']['title']

        starttime = parsed_json[i]['startTime']
        start = starttime / 1000.0
        start = time.strftime("%H:%M", time.localtime(start))

        endtime = parsed_json[i]['endTime']
        end = endtime / 1000.0
        end = time.strftime("%H:%M", time.localtime(end))

        times = start + " - " + end

        ok = times + "  -  " + show

        epg.append(ok)
        epg.append("\n")

        i += 1

    epg = ''.join(epg)

    if epg:

        xbmcgui.Dialog().textviewer(channel, epg)
    else:
        xbmcgui.Dialog().textviewer(channel, "Sorry no channel info at the moment!\nTry again later.")


get_epg(channel_id)


