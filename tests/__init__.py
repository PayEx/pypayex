# -*- coding: utf-8 -*-:
import unittest
from payex.pxagreement import PxCreateAgreement3Handler, PxAutoPay2Handler, PxDeleteAgreementHandler, PxAgreementCheckHandler
from payex.pxorder import PxOrderInitialize7Handler, PxOrderCompleteHandler, PxOrderCapture4Handler, PxOrderGetTransactionDetails2Handler
from payex.service import Payex
from payex.utils import XmlDictConfig

# Insert your keys here to test integration
MERCHANT_NUMBER = ''
ENCRYPTION_KEY = ''


class TestService(unittest.TestCase):
    """
    Test initialization of service.
    """

    def testServiceSetup(self):
        
        service = Payex(merchant_number='123', encryption_key='secret-string')
        
        # Check default values and setting of kwargs
        self.assertEquals(service.accountNumber, '123')
        self.assertEquals(service.encryption_key, 'secret-string')
        self.assertFalse(service.production)
        
        # Check that the order handlers are present
        self.assertTrue(isinstance(service.initialize, PxOrderInitialize7Handler))
        self.assertTrue(isinstance(service.complete, PxOrderCompleteHandler))
        self.assertTrue(isinstance(service.capture, PxOrderCapture4Handler))
        self.assertTrue(isinstance(service.get_transaction_details, PxOrderGetTransactionDetails2Handler))
       
        # Check that the agreement handlers are present
        self.assertTrue(isinstance(service.create_agreement, PxCreateAgreement3Handler))
        self.assertTrue(isinstance(service.delete_agreement, PxDeleteAgreementHandler))
        self.assertTrue(isinstance(service.check_agreement, PxAgreementCheckHandler))
        self.assertTrue(isinstance(service.autopay, PxAutoPay2Handler))

class TestOrders(unittest.TestCase):
    """
    Test the PxOrder methods.
    """
    
    def testPayment(self):
        """
        Test the initialize7 and complete method.
        """
        
        # Needs credentials to test
        self.assertTrue(all([MERCHANT_NUMBER, ENCRYPTION_KEY]))
        
        service = Payex(merchant_number=MERCHANT_NUMBER,
                        encryption_key=ENCRYPTION_KEY,
                        production=False
                       )
        
        # Initialize a payment
        response = service.initialize(purchaseOperation='AUTHORIZATION',
                                      price='5000',
                                      currency='NOK',
                                      vat='2500',
                                      orderID='test1',
                                      productNumber='123',
                                      description=u'This is a test. åâaä',
                                      clientIPAddress='127.0.0.1',
                                      clientIdentifier='USERAGENT=test&username=testuser',
                                      additionalValues='PAYMENTMENU=TRUE',
                                      returnUrl='http://example.org/return',
                                      view='PX',
                                      cancelUrl='http://example.org/cancel'
                                     )
        
        # Check the response
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertTrue('orderRef' in response)
        self.assertTrue(response['redirectUrl'].startswith('https://test-account.payex.com/MiscUI/PxMenu.aspx'))
        
        # Complete the order (even if it's not completed by user)
        response = service.complete(orderRef=response['orderRef'])
        
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'Order_OrderProcessing')

class TestAgreements(unittest.TestCase):
    """
    Test the PxAgreement methods.
    """
    
    def testCreateAgreement3(self):
        # Needs credentials to test
        self.assertTrue(all([MERCHANT_NUMBER, ENCRYPTION_KEY]))
        
        service = Payex(merchant_number=MERCHANT_NUMBER,
                        encryption_key=ENCRYPTION_KEY,
                        production=False,
                       )
        
        # Create an agreement
        response = service.create_agreement(merchantRef='oneclick',
                                 description='One-click shopping',
                                 purchaseOperation='AUTHORIZATION',
                                 maxAmount='100000',
                                )
        
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertTrue('agreementRef' in response)
        self.assertFalse('existingAgreementRef' in response)
        
        agreement_ref = response['agreementRef']
        
        response = service.initialize(purchaseOperation='AUTHORIZATION',
                                      price='5000',
                                      currency='NOK',
                                      vat='2500',
                                      orderID='test2',
                                      productNumber='123',
                                      description=u'This is a test with øæå.',
                                      clientIPAddress='127.0.0.1',
                                      clientIdentifier='USERAGENT=test&username=testuser',
                                      additionalValues='PAYMENTMENU=TRUE',
                                      returnUrl='http://example.org/return',
                                      view='PX',
                                      agreementRef=agreement_ref,
                                      cancelUrl='http://example.org/cancel'
                                     )
        
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertTrue('redirectUrl' in response)
        self.assertTrue(response['orderRef'] in response['redirectUrl'])

if __name__ == "__main__":
    unittest.main()
