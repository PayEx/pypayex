# -*- coding: utf-8 -*-:
import unittest
import os

from payex.pxagreement import PxCreateAgreement3Handler, PxAutoPay2Handler, PxDeleteAgreementHandler, PxAgreementCheckHandler
from payex.pxorder import PxOrderInitialize8Handler, PxOrderCompleteHandler, PxOrderCapture4Handler, PxOrderGetTransactionDetails2Handler, PxCancel2Handler
from payex.service import PayEx
from payex.utils import XmlDictConfig

# Insert your keys here to test integration
MERCHANT_NUMBER = os.environ['MERCHANT_NUMBER']
ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY']


class TestService(unittest.TestCase):
    """
    Test initialization of service.
    """

    def testServiceSetup(self):
        
        service = PayEx(merchant_number='123', encryption_key='secret-string')
        
        # Check default values and setting of kwargs
        self.assertEquals(service.accountNumber, '123')
        self.assertEquals(service.encryption_key, 'secret-string')
        self.assertFalse(service.production)
        
        # Check that the order handlers are present
        self.assertTrue(isinstance(service.initialize, PxOrderInitialize8Handler))
        self.assertTrue(isinstance(service.complete, PxOrderCompleteHandler))
        self.assertTrue(isinstance(service.capture, PxOrderCapture4Handler))
        self.assertTrue(isinstance(service.get_transaction_details, PxOrderGetTransactionDetails2Handler))
        self.assertTrue(isinstance(service.cancel, PxCancel2Handler))
       
        # Check that the agreement handlers are present
        self.assertTrue(isinstance(service.create_agreement, PxCreateAgreement3Handler))
        self.assertTrue(isinstance(service.delete_agreement, PxDeleteAgreementHandler))
        self.assertTrue(isinstance(service.check_agreement, PxAgreementCheckHandler))
        self.assertTrue(isinstance(service.autopay, PxAutoPay2Handler))
    
    def testStatelessness(self):
        """
        Test for an earlier bug, did not reset hash for new requests.
        """
        
        # Needs credentials to test
        self.assertTrue(all([MERCHANT_NUMBER, ENCRYPTION_KEY]))
        
        service = PayEx(
            merchant_number=MERCHANT_NUMBER, 
            encryption_key=ENCRYPTION_KEY, 
            production=False
        )
        
        # Create an agreement
        response = service.create_agreement(
            merchantRef='oneclick',
            description=u'One-click shopping æøåÆØÅ',
            purchaseOperation='SALE',
            maxAmount='100000',
        )
        
        # Create another agreement
        response = service.create_agreement(
            merchantRef='oneclick',
            description=u'One-click shopping æøåÆØÅ',
            purchaseOperation='SALE',
            maxAmount='100000',
        )
        
        # Ensure that the response is still valid
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertTrue('agreementRef' in response)

class TestOrders(unittest.TestCase):
    """
    Test the PxOrder methods.
    """
    
    def testPayment(self):
        """
        Test the initialize7 and complete methods.
        """
        
        # Needs credentials to test
        self.assertTrue(all([MERCHANT_NUMBER, ENCRYPTION_KEY]))
        
        service = PayEx(
            merchant_number=MERCHANT_NUMBER, 
            encryption_key=ENCRYPTION_KEY, 
            production=False
        )
        
        # Initialize a payment
        response = service.initialize(
            purchaseOperation='AUTHORIZATION',
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

        self.assertTrue(response['redirectUrl'].startswith('https://account.externaltest.payex.com/MiscUI/PxMenu.aspx'))
        
        # Try to complete the order (even if it's not started by user)
        response = service.complete(orderRef=response['orderRef'])
        
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'Order_OrderProcessing')
        
        # Get the transaction details
        response = service.get_transaction_details(transactionNumber='0')

        print(response)
        
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'NoRecordFound')
        
        # Try to capture a transaction
        response = service.capture(
            transactionNumber='0',
            amount='1000',
            vatAmount='250'
        )
        
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'NoRecordFound')
        
        # Try to cancel a transaction
        response = service.cancel(transactionNumber='1')
        
        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'NoRecordFound')


class TestAgreements(unittest.TestCase):
    """
    Test the PxAgreement methods.
    """
    
    def testAgreementHandlers(self):
        """
        Test the various agreement handlers.
        """
        
        # Needs credentials to test
        self.assertTrue(all([MERCHANT_NUMBER, ENCRYPTION_KEY]))
        
        service = PayEx(
            merchant_number=MERCHANT_NUMBER, 
            encryption_key=ENCRYPTION_KEY, 
            production=False
        )
        
        # Create an agreement
        response = service.create_agreement(
            merchantRef='oneclick',
            description=u'One-click shopping æøåÆØÅ',
            purchaseOperation='AUTHORIZATION',
            maxAmount='100000',
        )
        
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertTrue('agreementRef' in response)
        self.assertFalse('existingAgreementRef' in response)
        
        agreement_ref = response['agreementRef']
        
        # Initialize the payment
        response = service.initialize(
            purchaseOperation='AUTHORIZATION',
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
        
        # Try to complete the order (even if it's not started by user)
        response = service.complete(orderRef=response['orderRef'])
        
        print(response)

        self.assertEquals(type(response), XmlDictConfig)
        self.assertEquals(response['status']['errorCode'], 'Order_OrderProcessing')
        
        # AutoPay with the agreement
        response = service.autopay(
            purchaseOperation='SALE',
            agreementRef=agreement_ref,
            price='1000',
            productNumber='123',
            description=u'This is a test with øæå.',
            orderId='900'
        )
        
        self.assertEquals(response['status']['errorCode'], 'AgreementNotVerified')
        
        # Check the agreement
        response = service.check_agreement(agreementRef=agreement_ref)
        
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')
        self.assertEquals(response['agreementStatus'], '0')
        
        # Delete the agreement
        response = service.delete_agreement(agreementRef=agreement_ref)
        
        self.assertEquals(response['status']['description'], 'OK')
        self.assertEquals(response['status']['errorCode'], 'OK')


if __name__ == "__main__":
    unittest.main()
