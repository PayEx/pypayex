from payex.pxorder import PxOrderInitialize7Handler, PxOrderCompleteHandler


class Payex(object):
    """
    Base Payex service, with handlers.
    """
    
    def __init__(self, merchant_number, encryption_key, production=False):
        
        # Set account credentials
        self.accountNumber = merchant_number
        self.encryption_key = encryption_key
        self.production = production
        
        # Add handlers
        self.add_resource('initialize', PxOrderInitialize7Handler)
        self.add_resource('complete', PxOrderCompleteHandler)
    
    def add_resource(self, name, handler):
        """
        Initializes the handler with this service instance.
        """
        
        setattr(self, name, handler(self))
