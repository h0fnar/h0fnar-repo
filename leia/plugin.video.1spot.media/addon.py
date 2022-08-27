from urllib import urlencode
from urlparse import parse_qsl
import requests
import json
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import time
import re

_url = sys.argv[0]
_handle = int(sys.argv[1])

_scriptid_ = "plugin.video.1spot.media"
_addon_ = xbmcaddon.Addon(id=_scriptid_)
_script_path_ = "special://home/addons/" + _scriptid_ + "/resources/lib/"

icon = _addon_.getAddonInfo('icon')


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def main():
    xbmcplugin.setPluginCategory(_handle, "videos")

    name = ("Live TV and Radio")
    name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
    url = get_url(action='livestreams')
    is_folder = True
    list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    name = ("TV Shows")
    name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
    url = get_url(action='tvshows')
    is_folder = True
    list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    name = ("New Releases")
    name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
    url = get_url(action='newreleases')
    is_folder = True
    list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    name = ("Recommended")
    name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
    url = get_url(action='recommended')
    is_folder = True
    list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    get_cats()

    xbmcplugin.endOfDirectory(_handle)


def add_categories(name, href):
    name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
    url = get_url(action='categories', href=href)
    is_folder = True
    list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


cat_list = ("News\nnews\n",
            "Sports\nsports\n",
            "Entertainment\nentertainment\n",
            "Life Style\nlifestyle\n",
            "Talk Show\ndiscussion\n",
            "TVJ - VOD\nTVJ\n",
            "CVTV - VOD\nCVTV\n",
            "JNN - VOD\nJNN\n",
            "RETV - VOD\nRETV\n")


def get_cats():
    pattern = ("(.+?)\n(.+?)\n")
    for line in cat_list:
        regex = re.match(pattern, line)
        name = regex.group(1)
        href = regex.group(2)
        add_categories(name, href)


def list_categories(href, page):
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'episodes')

    start = page

    if href == ("TVJ") or href == ("CVTV") or href == ("JNN") or href == ("RETV"):
        link = ("https://www.1spotmedia.com/index.php/api/vod/get_category_videos?category=&page="+str(start)+"&channel="+href+"&from=&to=")
    else:
        link = ("https://www.1spotmedia.com/index.php/api/vod/get_category_videos?category="+href+"&page="+str(start)+"&channel=&from=&to=")

    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)
    max_guesses = le - 1
    i = 0

    while i <= max_guesses:

        title = parsed_json[i]['title']
        try:
            airdate = parsed_json[i]['aired_date']
            airdate = airdate / 1000
            aired = time.strftime("%Y-%m-%d", time.gmtime(airdate))
            date_sort = time.strftime("%d.%m.%Y", time.gmtime(airdate))
        except:
            airdate = False

        stream = parsed_json[i]['HLSStream']['url']

        img = parsed_json[i]['PosterH']['downloadUrl']

        description = parsed_json[i]['description']

        url = get_url(action='play', stream=stream)
        is_folder = False
        list_item = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb' : img})

        info = {
                    'plot': description,
                    'aired': aired,
                    'date': str(date_sort),
                    }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)

    start = int(start)
    start += 1
    if href == ("TVJ") or href == ("CVTV") or href == ("JNN") or href == ("RETV"):
        link = ("https://www.1spotmedia.com/index.php/api/vod/get_category_videos?category=&page="+str(start)+"&channel="+href+"&from=&to=")
    else:
        link = ("https://www.1spotmedia.com/index.php/api/vod/get_category_videos?category="+href+"&page="+str(start)+"&channel=&from=&to=")
    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)
    if le:
        url = get_url(action='nextpage',href=href, page=start)
        is_folder = True
        name = ("Next Page")
        name = "[COLOR darkorchid][B]" + name + "[/B][/COLOR]"
        list_item = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(_handle)


def list_channels():
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'videos')

    search = 'https://www.1spotmedia.com/index.php/api/vod/get_live_streams'
    html = requests.get(search)
    parsed_json = json.loads(html.text)
    results = parsed_json[1]['title']

    le = len(parsed_json)
    max_guesses = le - 1
    i = 0

    while i <= max_guesses:

        channel = parsed_json[i]['title']
        channel_name = channel
        channel_id = parsed_json[i]['_id']

        try:
            epg = get_epg(channel_id)
        except:
            epg = ("Sorry no channel info!")

        channel = "[COLOR darkorchid][B]" + channel + "[/B][/COLOR]"
        channel = channel + "  -  " + epg
    
        logo = parsed_json[i]['ChannelLogoSmall']['url']

        stream = parsed_json[i]['HLSStream']['url']

        url = get_url(action='play', stream=stream)
        is_folder = False
        list_item = xbmcgui.ListItem(channel, iconImage=logo, thumbnailImage=logo)
        list_item.setProperty('IsPlayable', 'true')

        list_item.addContextMenuItems([
                                    ("[COLOR darkorchid]Show Stream Schedule[/COLOR]", "XBMC.RunScript("+_script_path_+"channel_epg.py,"+channel_name+","+str(channel_id)+")")
                                    ])

        list_item.setInfo('video', {'mediatype': 'video'}) #?

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.endOfDirectory(_handle)


def list_series():
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'tvshows')

    search = 'https://www.1spotmedia.com/index.php/api/vod/get_all_series?page=0'

    html = requests.get(search)
    parsed_json = json.loads(html.text) 

    results = parsed_json[1]['title']
    le = len(parsed_json)
    max_guesses = le - 1
    i = 0   

    while i <= max_guesses: 

        title = parsed_json[i]['title']
        description = parsed_json[i]['description']
        if not description:
            description = ("Sorry no description!")
        description = description.replace("\n\n", ' ')
        description = description.strip()
        description = description.encode('utf-8')

        try:
            seasons_count = parsed_json[i]['seasons_count']
            episodes_count = parsed_json[i]['episodes_count']
            episodes_seasons = "Seasons: " + str(seasons_count) + "   " + "Episodes: " + str(episodes_count)
            episodes_seasons = "[COLOR grey][B]" + episodes_seasons + "[/B][/COLOR]"

            description = episodes_seasons + "\n\n" + description
            description = description.encode('utf-8')
        except:
            pass

        try:
            banner = parsed_json[i]['PosterH']['downloadUrl']
        except:
            banner = icon
        try:
            poster = parsed_json[i]['PosterV']['downloadUrl']
        except:
            poster = icon

        try:
            sid = parsed_json[i]['_id']
        except:
            pass

        try:
            vod_category = parsed_json[i]['vod_category'][0]
        except:
            vod_category = "no vod_category"

        if vod_category == "no vod_category":
            try:
                keywords = parsed_json[i]['keywords'][0]
            except:
                keywords = "TV Show"
        else:
            keywords = vod_category
        genre = keywords.title()

        url = get_url(action='season', sid=sid, poster=poster, banner=banner, description=description)
        is_folder = True
        list_item = xbmcgui.ListItem(title, iconImage=poster, thumbnailImage=poster)
        list_item.setArt({'fanart': banner, 'poster' : poster})

        info = {
                        'plot': description,
                        'genre': genre,
                        'title': title,
                        }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 

        i += 1

    xbmcplugin.endOfDirectory(_handle)


def list_season(sid, poster, banner, description):
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'tvshows')

    main = ("https://www.1spotmedia.com/index.php/api/vod/get_seasons_episodes?id=")
    search = main + sid 
   
    try:
        html = requests.get(search)
        parsed_json = json.loads(html.text)
    except:
        pass

    results = parsed_json['seasons']

    nkeys =[]
    for key, value in results.items():
        nkeys.append(key)

    le = len(results)
    max_guesses = le - 1
    i = 0   

    while i <= max_guesses:
        s_id = nkeys[i]
        staffel = parsed_json['seasons'][s_id]['title']

        url = get_url(action='episode', sid=sid, poster=poster, banner=banner, season=s_id)
        is_folder = True
        list_item = xbmcgui.ListItem(staffel, iconImage=poster, thumbnailImage=poster)
        list_item.setArt({'fanart': banner, 'poster' : poster})

        info = {
                        'plot': description,
                        'genre': "TV Show",
                        }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.endOfDirectory(_handle)


def list_episodes(sid, poster, banner, season):
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'episodes')

    main = ("https://www.1spotmedia.com/index.php/api/vod/get_seasons_episodes?id=")
    search = main + sid

    try:
        html = requests.get(search)
        parsed_json = json.loads(html.text)
    except:
        pass

    results = parsed_json['seasons'][season]['episodes']

    le = len(results)
    max_guesses = le - 1
    i = 0   

    while i <= max_guesses:

        title = parsed_json['seasons'][season]['episodes'][i]['media']['title']
        
        results_2 = parsed_json['seasons'][season]['episodes'][i]['media']['content']

        le_2 = len(results_2)
        max_guesses_2 = le_2 - 1
        x = 0

        fanart = False

        while x <= max_guesses_2:

            content = parsed_json['seasons'][season]['episodes'][i]['media']['content'][x]['downloadUrl']
            if ".jpg" in content or ".png" in content:
                fanart = content

            if ".m3u8" in content:
                streams = content
                if ".m3u8?" not in streams:
                    stream = streams

            x += 1

            if not fanart:
                fanart = banner
   
        try:
            description = parsed_json['seasons'][season]['episodes'][i]['media']['description']
            if not description:
                description = ("No description found!")
        except:
            description = ("No description found!")
      
        try:
            aired_date = parsed_json['seasons'][season]['episodes'][i]['media']['aired_date']
            aired_date = aired_date / 1000
            aired = time.strftime("%Y-%m-%d", time.gmtime(aired_date))
            date_sort = time.strftime("%d.%m.%Y", time.gmtime(aired_date))
        except:
            aired = False
            date_sort = False

        url = get_url(action='play', stream=stream)
        is_folder = False
        list_item = xbmcgui.ListItem(title, iconImage=poster, thumbnailImage=poster)
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'fanart': banner, 'thumb' : fanart, 'poster' : poster})

        info = {
                    'plot': description,
                    'aired': aired,
                    'date': str(date_sort),
                    }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(_handle)


def new_release():
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'episodes')

    link = ("https://www.1spotmedia.com/index.php/api/vod/get_new_release")
    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)
    max_guesses = le - 1
    i = 0

    while i <= max_guesses:

        title = parsed_json[i]['title']

        airdate = parsed_json[i]['aired_date']
        airdate = airdate / 1000
        aired = time.strftime("%Y-%m-%d", time.gmtime(airdate))
        date_sort = time.strftime("%d.%m.%Y", time.gmtime(airdate))

        stream = parsed_json[i]['HLSStream']['url']

        img = parsed_json[i]['PosterH']['downloadUrl']

        description = parsed_json[i]['description']

        url = get_url(action='play', stream=stream)
        is_folder = False
        list_item = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb' : img})

        info = {
                    'plot': description,
                    'aired': aired,
                    'date': str(date_sort),
                    }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(_handle)


def recommended():
    xbmcplugin.setPluginCategory(_handle, "videos")
    xbmcplugin.setContent(_handle, 'episodes')

    link = ("https://www.1spotmedia.com/index.php/api/vod/get_recommended")
    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)
    max_guesses = le - 1
    i = 0

    while i <= max_guesses:

        title = parsed_json[i]['title']

        airdate = parsed_json[i]['aired_date']
        airdate = airdate / 1000
        aired = time.strftime("%Y-%m-%d", time.gmtime(airdate))
        date_sort = time.strftime("%d.%m.%Y", time.gmtime(airdate))

        stream = parsed_json[i]['HLSStream']['url']

        img = parsed_json[i]['PosterH']['downloadUrl']

        description = parsed_json[i]['description']

        url = get_url(action='play', stream=stream)
        is_folder = False
        list_item = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb' : img})

        info = {
                    'plot': description,
                    'aired': aired,
                    'date': str(date_sort),
                    }

        list_item.setInfo('video', info)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        i += 1

    xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(_handle)


def get_epg(channel_id):
    main = ("https://www.1spotmedia.com/index.php/api/epg/get_epg_timeline_by_id?id=")
    link = main + channel_id
    html = requests.get(link)
    parsed_json = json.loads(html.text)

    le = len(parsed_json)
    max_guesses = le - 1
    i = 0

    ts = time.time()

    while i <= max_guesses:
        show = parsed_json[i]['program']['title']

        starttime = parsed_json[i]['startTime']
        start = starttime / 1000.0
        start_hm = time.strftime("%H:%M", time.localtime(start))

        endtime = parsed_json[i]['endTime']
        end = endtime / 1000.0
        end_hm = time.strftime("%H:%M", time.localtime(end))

        start_end = start_hm + " - " +  end_hm

        if start <= ts <= end:
            tt = 100 / (end - start) * (end - ts)
            percent = str(tt)
            head, sep, tail = percent.partition('.')
            percent = head
            percent = (int(percent) - 100)
            percent = str(percent)
            percent = percent.lstrip("-")
            show = "[COLOR darkorchid][B]" + show + "[/B][/COLOR]"
            epg = "[" + percent + "%] - " + show + " - " + "[" + start_end + "]"
            pass

        i += 1

    return epg


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))

    if params:

        if params['action'] == 'livestreams':
            list_channels()

        elif params['action'] == 'tvshows':
            list_series()

        elif params['action'] == 'newreleases':
            new_release()

        elif params['action'] == 'recommended':
            recommended()


        elif params['action'] == 'categories':
            href = (params['href'])
            list_categories(href, 0)

        elif params['action'] == 'nextpage':
            href = (params['href'])
            page = (params['page'])
            list_categories(href, page)


        elif params['action'] == 'season':
            sid = (params['sid'])
            poster = (params['poster'])
            banner = (params['banner'])
            description = (params['description'])           
            list_season(sid, poster, banner, description)

        elif params['action'] == 'episode':
            sid = (params['sid'])
            poster = (params['poster'])
            banner = (params['banner'])
            season = (params['season'])
            list_episodes(sid, poster, banner, season)
       
        elif params['action'] == 'play':
            stream = (params['stream'])
            play_video(params['stream'])

        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))

    else:
        main()
        

if __name__ == '__main__':
    router(sys.argv[2][1:])

