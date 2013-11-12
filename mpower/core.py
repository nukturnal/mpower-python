"""Payment processing logic for DirectPay, DirectCard, Invoice, and OPR"""
import os
import urllib2
try:
    import simplejson as json
except ImportError:
    import json

# MPower HTTP API version
API_VERSION = "v1"
#Sandbox Endpoint
SANDBOX_ENDPOINT="https://app.mpowerpayments.com/sandbox-api/%s/" % API_VERSION 
#Live Endpoint
LIVE_ENDPOINT="https://app.mpowerpayments.com/api/%s/" % API_VERSION
# user-agent headers
MP_USER_AGENT="MPower-Python client library - v0.1.0"

class Payment(object):
    def __init__(self, configs, debug=False):
        """Base class for all the other payment libraries"""
        self.config = {
            'MP_Master_Key': configs.get('MP_Master_Key',
                                         os.environ.get('MP_Master_Key',)), 
            'MP_Private_Key': configs.get('MP_Private_Key', 
                                          os.environ.get('MP_Private_Key')),
            'MP_Token': configs.get('MP_Token', 
                                    os.environ.get('MP_Token'))
        }
        # request headers
        self._headers = {'User-Agent': MP_USER_AGENT, 
                         "Content-Type": "application/json"}
        # response object
        self._response = None
        # data to send to server
        self._data = None 
        self.debug = debug

    def _process(self, resource=None, data=None):
        """Processes the current ransaction

        Sends an HTTP request to the currently active endpoint of the MPower API
        """
        req = urllib2.Request(self.get_rsc_endpoint(resource), data or self._data, self.headers)
        response = urllib2.urlopen(req)
        if response.code == 200:
            self._response = json.loads(response.read())
            if self._response['response_code'] == 00:
                return (True, self._response)
            else:
                return (False, None)
        return (response.code, "Request Failed")

    @property
    def headers(self):
        """Returns the client's Request headers"""
        return dict(self.config.items() + self._headers.items())

    def add_header(header):
        """Add a custom HTTP header to the client's request headers"""
        if type(header) is dict:
            self._headers.update(header)
        else:
            raise ValueError("Dictionary expected, got '%s' instead" % type(header))
            
    def get_rsc_endpoint(self, rsc):
        """Returns the HTTP API URL for current payment transaction"""
        if self.debug:            
            return SANDBOX_ENDPOINT + rsc
        return LIVE_ENDPOINT + rsc
