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

def playLiveTv(manifest_url, package_code, infolabels='', parental_rating=0):
    #hardcoded apixId for live content
    apix_id = 'livechannel_127'

    info_tag = None
    if infolabels != '':
        info_tag = ast.literal_eval(infolabels)        

    skyticket.play(manifest_url, package_code, parental_rating=parental_rating, info_tag=info_tag, apix_id=apix_id)