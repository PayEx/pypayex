from suds.client import Client

from payex.handlers import BaseHandler


class PxOrderHandler(BaseHandler):
    """
    Base handler for PxOrder methods.
    """
    
    def __call__(self, *args, **kwargs):
        
        # Set the parameters on object
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        
        # Which WDSL URL to use
        if self._service.production:
            self._wdsl_url = 'https://external.payex.com/pxorder/pxorder.asmx?WSDL'
        else:
            self._wdsl_url = 'https://test-external.payex.com/pxorder/pxorder.asmx?WSDL'
        
        # Initialize the WDSL schema and set endpoint
        self._client = Client(self._wdsl_url)

###################
# METHOD HANDLERS #
###################

class PxOrderInitialize7Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/initialize7/
    """
    
    field_order = [
        'accountNumber', 
        'purchaseOperation', 
        'price', 
        'priceArgList', 
        'currency', 
        'vat', 
        'orderID', 
        'productNumber', 
        'description', 
        'clientIPAddress', 
        'clientIdentifier', 
        'additionalValues', 
        'externalID', 
        'returnUrl', 
        'view', 
        'agreementRef', 
        'cancelUrl', 
        'clientLanguage',
    ]
    
    def __call__(self, *args, **kwargs):
        
        super(PxOrderInitialize7Handler, self).__call__(*args, **kwargs)
        
        # Set SOAP endpoint and send request
        self._endpoint = self._client.service.Initialize7
        
        return self._send_request()

class PxOrderCompleteHandler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/complete-2/
    """
    
    field_order = [
        'accountNumber', 
        'orderRef', 
    ]
    
    def __call__(self, *args, **kwargs):
        
        super(PxOrderCompleteHandler, self).__call__(*args, **kwargs)
        
        # Set SOAP endpoint and send request
        self._endpoint = self._client.service.Complete
        
        return self._send_request()
