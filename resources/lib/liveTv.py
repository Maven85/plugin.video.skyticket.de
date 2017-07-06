import sys
import requests
import xbmcaddon
import xbmcgui
import xbmcplugin
import ast
from skyticket import SkyTicket

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
skyticket = SkyTicket()

def playLiveTv(manifest_url, package_code, infolabels=''):
    #hardcoded apixId for live content
    apix_id = 'livechannel_127'

    info_tag = None
    if infolabels != '':
        info_tag = ast.literal_eval(infolabels)

    skyticket.play(manifest_url, package_code, info_tag=info_tag, apix_id=apix_id)

def play_live_tv(epg_channel_id):
    # Get Current running event on channel
    current_event = skyticket.getCurrentEvent(epg_channel_id)

    # If there is a running event play it
    if current_event is not False:
        event_id = current_event['id']
        playInfo = skyticket.getEventPlayInfo(event_id, epg_channel_id)

        apix_id = playInfo['apixId']
        manifest_url = playInfo['manifestUrl']

        # Login to get session
        login = skyticket.login()
        session_id = skyticket.sessionId

        # create init data for licence acquiring
        init_data = skyticket.get_init_data(session_id, apix_id)

        # Create list item with inputstream addon
        li = xbmcgui.ListItem(path=manifest_url)
        info = {
            'mediatype': 'movie',
        }
        li.setInfo('video', info)
        li.setProperty('inputstream.adaptive.license_type', skyticket.license_type)
        li.setProperty('inputstream.adaptive.manifest_type', 'ism')
        if init_data:
            li.setProperty('inputstream.adaptive.license_key', skyticket.licence_url)
            li.setProperty('inputstream.adaptive.license_data', init_data)
        li.setProperty('inputstreamaddon', 'inputstream.adaptive')

        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=li)
    else:
        xbmcgui.Dialog().notification('Kein laufendes Event', 'Auf diesem Kanal ist kein laufendes Event vorhanden.', icon=xbmcgui.NOTIFICATION_WARNING)