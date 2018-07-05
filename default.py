#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urlparse
import ast
import resources.lib.vod as vod
import resources.lib.clips as clips
import resources.lib.liveTv as liveTv
from skyticket import SkyTicket

import navigation as nav
import watchlist

plugin_base_url = sys.argv[0]
params = dict(urlparse.parse_qsl(sys.argv[2][1:]))

addon_handle = int(sys.argv[1])
skyticket = SkyTicket(addon_handle)

vod.skyticket = skyticket
nav.skyticket = skyticket
clips.skyticket = skyticket
liveTv.skyticket = skyticket
watchlist.skyticket = skyticket


def getDictFromString(str):
    return ast.literal_eval(str) if str else None


# Router for all plugin actions
if 'action' in params:

    print params

    if params['action'] == 'playVod':
        vod.playAsset(params['vod_id'], infolabels=getDictFromString(params.get('infolabels', None)), art=getDictFromString(params.get('art', None)), parental_rating=int(params.get('parental_rating', 0)))
    elif params['action'] == 'playClip':
        clips.playClip(params['id'])
    elif params['action'] == 'playLive':
        liveTv.playLiveTv(params['manifest_url'], package_code=params.get('package_code'), infolabels=getDictFromString(params.get('infolabels', None)), art=getDictFromString(params.get('art', None)), parental_rating=int(params.get('parental_rating', 0)))
    elif params['action'] == 'listLiveTvChannelDirs':
        nav.listLiveTvChannelDirs()
    elif params['action'] == 'listLiveTvChannels':
        channeldir_name = ''
        if 'channeldir_name' in params:
            channeldir_name = params['channeldir_name']
        nav.listLiveTvChannels(channeldir_name)

    elif params['action'] == 'watchlist':
        if 'list' in params:
            page = 0
            if 'page' in params:
                page = params['page']
            watchlist.listWatchlist(params['list'], page=page)
        else:
            watchlist.rootDir()
    elif params['action'] == 'watchlistAdd':
        watchlist.addToWatchlist(params['id'], params['assetType'])
    elif params['action'] == 'watchlistDel':
        watchlist.deleteFromWatchlist(params['id'])

    elif params['action'] == 'search':
        nav.search()

    elif params['action'] == 'listPage':
        if 'id' in params:
             nav.listPage(params['id'])
        elif 'path' in params:
            nav.listPath(params['path'])

    elif params['action'] == 'listSeries':
        nav.listSeasonsFromSeries(params['id'])
    elif params['action'] == 'listSeason':
        nav.listEpisodesFromSeason(params['series_id'], params['id'])

    elif params['action'] == 'parentalSettings':
        nav.showParentalSettings()

    elif params['action'] == 'login':
        skyticket.setLogin()

    elif params['action'] == 'clearCache':
        nav.clearCache()

else:
    nav.rootDir()