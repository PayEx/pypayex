from payex.handlers import BaseHandler

class PxOrderHandler(BaseHandler):
    """
    Base handler for PxOrder methods.
    """

    production_url = 'https://external.payex.com/pxorder/pxorder.asmx?WSDL'
    testing_url = 'https://test-external.payex.com/pxorder/pxorder.asmx?WSDL'

    def __call__(self, *args, **kwargs):
        
        # Set the parameters on object
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self._client = self.client_factory()

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
        
        # Set endpoint and send request
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
        
        # Set endpoint and send request
        self._endpoint = self._client.service.Complete
        
        return self._send_request()

class PxOrderCapture4Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/capture4/
    """
    
    field_order = [
        'accountNumber',
        'transactionNumber',
        'amount',
        'orderId',
        'vatAmount',
        'additionalValues',
    ] 
    
    def __call__(self, *args, **kwargs):
        
        super(PxOrderCapture4Handler, self).__call__(*args, **kwargs)
        
        # Set endpoint and send request
        self._endpoint = self._client.service.Capture4
        
        return self._send_request()

class PxOrderGetTransactionDetails2Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/gettransactiondetails2/
    """

    field_order = [
        'accountNumber',
        'transactionNumber'
    ]

    def __call__(self, *args, **kwargs):
        
        super(PxOrderGetTransactionDetails2Handler, self).__call__(*args, **kwargs)
        
        # Set endpoint and send request
        self._endpoint = self._client.service.GetTransactionDetails2
        
        return self._send_request()

class PxCancel2Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/cancel2/
    """
    
    field_order = [
        'accountNumber',
        'transactionNumber'
    ]
    
    def __call__(self, *args, **kwargs):
        
        super(PxCancel2Handler, self).__call__(*args, **kwargs)
        
        # Set endpoint and send request
        self._endpoint = self._client.service.Cancel2
        
        return self._send_request()
