"""Payment processing logic for DirectPay, DirectCard, Invoice, and OPR"""
import os
import sys
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


class MPowerError(Exception):
    """Base Exception class"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Payment(object):
    def __init__(self, configs={}, debug=False):
        """Base class for all the other payment libraries"""
        # fallback on system environment variables, 
        self.config = {
            'MP-Master-Key': configs.get('MP-Master-Key',
                                         os.environ.get('MP_Master_Key',)), 
            'MP-Private-Key': configs.get('MP-Private-Key', 
                                          os.environ.get('MP_Private_Key')),
            'MP-Token': configs.get('MP-Token', 
                                    os.environ.get('MP_Token'))
        }
        # fallback on global MP_ACCESS_TOKENS runtime variable
        if not all(self.config.values()):
            self.config.update(self.runtime_configs)

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
        # Return None(resolves to a GET request) if no data is to be sent
        _data = json.dumps(self._data) if self._data else None
        # use object's accumulated data if no data is passed
        _data = data if data else _data
        req = urllib2.Request(self.get_rsc_endpoint(resource), 
                              json.dumps(_data), self.headers)
        response = urllib2.urlopen(req)
        if response.code == 200:
            self._response = json.loads(response.read())
            if int(self._response['response_code']) == 00:
                return (True, self._response)
            else:
                return (False, self._response['response_text'])
        return (response.code, "Request Failed")

    @property
    def headers(self):
        """Returns the client's Request headers"""
        return dict(self.config.items() + self._headers.items())

    def add_header(self, header):
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

    @property
    def runtime_configs(self):
        """Returns the MP_ACCESS_TOKENS runtime variable"""
        var_name = "MP_ACCESS_TOKENS"
        calling_frame = sys._getframe().f_back
        var_val = calling_frame.f_locals.get(var_name, 
                                             calling_frame.f_globals.get(var_name, None))
        return var_val if var_val else {}
