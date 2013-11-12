"""MPower Payments Store"""
from .core import Payment

class Store(object):
    """MPower Store
    
    Creates a storw object for MPower Payments transactions
    """
    def __init__(self, info={}):
        self.info = {"name": info.get("name"),
                     "tagline": info.get("tagline"),
                     "postal_address": info.get("postal_address"),
                     "phone": info.get("phone"),
                     "logo_url": info.get("logo_url"),
                     "website_url": info.get("website_url")
        }
