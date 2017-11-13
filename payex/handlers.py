try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from xml.etree import ElementTree
import hashlib
import logging
import os

from suds import WebFault, client

from payex.utils import XmlDictConfig, normalize_dictionary_values, smart_str

logger = logging.getLogger(__name__)


class BaseHandler(object):
    """
    A base handler for SOAP operations. Not to be used directly.
    """
    
    def __init__(self, service):
        self._service = service
    
    def _get_params(self):
        """
        Generate SOAP parameters.
        """
        
        params = {'accountNumber': self._service.accountNumber}
        
        # Include object variables that are in field_order
        for key, val in self.__dict__.iteritems():
            if key in self.field_order:
                
                # Turn into Unicode
                if isinstance(val, str,):
                    val = val.decode('utf8')
                
                params[key] = val
        
        # Set missing parameters as empty strings
        for key in self.field_order:
            if key not in params:
                params[key] = u''
        
        # Parameter sorting method
        def order_keys(k):
            if k[0] in self.field_order:
                return self.field_order.index(k[0])
            return len(self.field_order) + 1
        
        # Sort the ordered dictionary
        params = OrderedDict(sorted(params.items(), key=order_keys))
        
        # Add hash to dictionary if present
        if hasattr(self, 'hash') and self.hash is not None:
            params['hash'] = self.hash
        
        return params
    
    def _generate_hash(self):
        """
        Generates a hash based on the specific fields for the method.
        """
        
        self.hash = None
        str_hash = ''
        
        for key, val in self._get_params().iteritems():
            str_hash += smart_str(val)
        
        # Append the encryption string
        str_hash += self._service.encryption_key
        
        # Set md5 hash on the object
        self.hash = hashlib.md5(str_hash).hexdigest()
    
    def _send_request(self):
        """
        Make the SOAP request and convert the result to a dictionary.
        """
        
        # Generate the hash variable and parameters
        self._generate_hash()
        params = self._get_params()
        
        # Make the SOAP request
        try:
            resp = self._endpoint(**params)
            logger.debug(resp)
        except WebFault, e:
            logger.exception('An error occurred while making the SOAP request.')
            return None
        
        # Convert XML response into a dictionary
        self.response = XmlDictConfig(ElementTree.XML(smart_str(resp)))
        
        # Normalize dictionary values
        self.response = normalize_dictionary_values(self.response)
        
        # Log all non OK status codes
        if self.response['status']['errorCode'] != 'OK':
            logger.error(resp)
        
        return self.response
    
    def client_factory(self):
        """
        Custom client factory to set proxy options.
        """
        
        if self._service.production:
            url = self.production_url
        else:
            url = self.testing_url
        
        proxy_options = dict()
        https_proxy_setting = os.environ.get('PAYEX_HTTPS_PROXY') or os.environ.get('https_proxy')
        http_proxy_setting = os.environ.get('PAYEX_HTTP_PROXY') or os.environ.get('http_proxy')
        
        if https_proxy_setting:
            proxy_options['https'] = https_proxy_setting
        if http_proxy_setting:
            proxy_options['http'] = http_proxy_setting
        
        return client.Client(url, proxy=proxy_options)
