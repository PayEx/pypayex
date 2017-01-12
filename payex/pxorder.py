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

class PxOrderInitialize8Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/initialize8/
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
        
        super(PxOrderInitialize8Handler, self).__call__(*args, **kwargs)
        
        # Set endpoint and send request
        self._endpoint = self._client.service.Initialize8
        
        return self._send_request()


class PxAddSingleOrderLine2Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/addsingleorderline2/
    """
    
    field_order = [
        'accountNumber', 
        'orderRef', 
        'itemNumber', 
        'itemDescription1', 
        'itemDescription2', 
        'itemDescription3', 
        'itemDescription4', 
        'itemDescription5', 
        'quantity', 
        'amount', 
        'vatPrice', 
        'vatPercent',
    ]
    
    def __call__(self, *args, **kwargs):
        
        super(PxAddSingleOrderLine2Handler, self).__call__(*args, **kwargs)
        
        # Set endpoint and send request
        self._endpoint = self._client.service.AddSingleOrderLine2
        
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

class PxCredit5Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/credit5/
    """

    field_order = [
        'accountNumber',
        'transactionNumber',
        'amount',
        'orderId',
        'vatAmount',
        'additionalValues'
    ]

    def __call__(self, *args, **kwargs):

        super(PxCredit5Handler, self).__call__(*args, **kwargs)

        # Set endpoint and send request
        self._endpoint = self._client.service.Credit5

        return self._send_request()


class PxPurchaseInvoiceCorporateHandler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/purchaseinvoicecorporate/
    """

    field_order = [
        'accountNumber',
        'orderRef',
        'companyRef',
        'companyName',
        'streetAddress',
        'coAddress',
        'postalCode',
        'city',
        'country',
        'organizationNumber',
        'phoneNumber',
        'email',
        'productCode',
        'creditcheckRef',
        'mediaDistribution',
        'invoiceText',
        'invoiceDate',
        'invoiceDueDays',
        'invoiceNumber',
        'invoiceLayout',
    ]

    def __call__(self, *args, **kwargs):

        super(PxPurchaseInvoiceCorporateHandler, self).__call__(*args, **kwargs)

        # Set endpoint and send request
        self._endpoint = self._client.service.PurchaseInvoiceCorporate

        return self._send_request()


class PxCheck2Handler(PxOrderHandler):
    """
    Reference:
    http://www.payexpim.com/technical-reference/pxorder/check2/
    """

    field_order = [
        'accountNumber',
        'transactionNumber'
    ]

    def __call__(self, *args, **kwargs):

        super(PxCheck2Handler, self).__call__(*args, **kwargs)

        # Set endpoint and send request
        self._endpoint = self._client.service.Check2

        return self._send_request()
