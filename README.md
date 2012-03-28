# pypayex

pypayex is a Python module for interacting with the PayEx Soap API.

The PayEx implementation manual is available here:
http://www.payexpim.com/

## Installation

Install `pypayex` (available on PyPi):

	pip install pypayex

Requires the `suds` SOAP library, and `ordereddict` on Python < 2.7.

## Usage

	from payex.service import PayEx
	
	service = PayEx(merchant_number='YOUR_MERCHANT_NUMER', encryption_key='YOUR_ENCRYPTION_KEY', production=False)
	
	# Initialize payment
	response = service.initialize(
		purchaseOperation='SALE',
		price='5000',
		currency='NOK',
		vat='2500',
		orderID='test1',
		productNumber='123',
		description=u'This is a test.',
		clientIPAddress='127.0.0.1',
		clientIdentifier='USERAGENT=test&username=testuser',
		additionalValues='PAYMENTMENU=TRUE',
		returnUrl='http://example.org/return/',
		view='PX',
		cancelUrl='http://example.org/cancel/'
	)

User performs the payment on the URL in `response['redirectURL']`, and is redirected back to the `returnUrl`.

	# When user is redirected back to the returnUrl, check the status of the transaction
	response = service.complete(orderRef='GENERATED_ORDER_REF')
	
	# Transaction was successfully performed
	response['status']['errorCode'] == 'OK' and response['transactionStatus'] == '0'
