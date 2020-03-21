"""
Custom component for Home Assistant to enable sending messages via Notify Line API.


Example configuration.yaml entry:

notify:
  - name: line_notification
    platform: notify_line
    access_token: 'line_access_token'    
    
With this custom component loaded, you can send messaged to line Notify.
"""

import requests
import logging
import voluptuous as vol
 
from aiohttp.hdrs import AUTHORIZATION
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ACCESS_TOKEN 
from homeassistant.components.notify import (
    ATTR_DATA, PLATFORM_SCHEMA, BaseNotificationService)

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://notify-api.line.me/api/notify'
ATTR_FILE = 'file'
ATTR_URL = 'url'
ATTR_STKPKGID ='stkpkgid'
ATTR_STKID ='stkid'
IMAGEFULLSIZE = 'imageFullsize'
IMAGETHURMBNAIL = 'imageThumbnail'
IMAGEFILE = 'imageFile'
STKPKID = 'stickerPackageId'
STKID = 'stickerId'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
})

def get_service(hass, config, discovery_info=None):
    """Get the Line notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN )
    return LineNotificationService(access_token)
                                           
class LineNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, access_token):
        """Initialize the service."""
        self.access_token = access_token                                           
        
    def send_message(self, message="", **kwargs):
        """Send some message."""
        data = kwargs.get(ATTR_DATA, None) 
        url = data.get(ATTR_URL) if data is not None and ATTR_URL in data else None
        file = {IMAGEFILE:open(data.get(ATTR_FILE),'rb')} if data is not None and ATTR_FILE in data else None
        stkpkgid = data.get(ATTR_STKPKGID) if data is not None and ATTR_STKPKGID in data and ATTR_STKID in data else None
        stkid = data.get(ATTR_STKID) if data is not None and ATTR_STKPKGID in data and ATTR_STKID in data else None        
        headers = {AUTHORIZATION:"Bearer "+ self.access_token}

        payload = ({
                    'message':message,
                    IMAGEFULLSIZE:url,
                    IMAGETHURMBNAIL:url,
                    STKPKID:stkpkgid,
                    STKID:stkid,          
                }) 
       
        r=requests.Session().post(BASE_URL, headers=headers, files=file, data=payload)
        if r.status_code  != 200:
            _LOGGER.error(r.text)
