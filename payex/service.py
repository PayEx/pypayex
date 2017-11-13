from payex import pxagreement
from payex import pxorder


class PayEx(object):
    """
    Base PayEx service, with handlers.
    """
    
    def __init__(self, merchant_number, encryption_key, production=False):
        
        # Set account credentials
        self.accountNumber = merchant_number
        self.encryption_key = encryption_key
        self.production = production
        
        # Add agreement handlers
        self.add_resource('create_agreement', pxagreement.PxCreateAgreement3Handler)
        self.add_resource('delete_agreement', pxagreement.PxDeleteAgreementHandler)
        self.add_resource('check_agreement', pxagreement.PxAgreementCheckHandler)
        self.add_resource('autopay', pxagreement.PxAutoPay2Handler)
        
        # Add order handlers
        self.add_resource('initialize', pxorder.PxOrderInitialize8Handler)
        self.add_resource('complete', pxorder.PxOrderCompleteHandler)
        self.add_resource('capture', pxorder.PxOrderCapture4Handler)
        self.add_resource('get_transaction_details', pxorder.PxOrderGetTransactionDetails2Handler)
        self.add_resource('cancel', pxorder.PxCancel2Handler)
        self.add_resource('credit', pxorder.PxCredit5Handler)
        self.add_resource('check', pxorder.PxCheck2Handler)
        self.add_resource('add_single_order_line', pxorder.PxAddSingleOrderLine2Handler)
        self.add_resource('purchase_invoice_corporate', pxorder.PxPurchaseInvoiceCorporateHandler)
    
    def add_resource(self, name, handler):
        """
        Initializes the handler with this service instance.
        """
        
        setattr(self, name, handler(self))
