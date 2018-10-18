from helpers.http_client import HttpClient
from helpers.http_error_handler import HttpErrorHandler
from models.lookup_result import LookupResult
from models.keyword import Keyword
from models.out_message import OutMessage
from models.strex_merchant_id import StrexMerchantId

name = "target365-sdk"

class ApiClient:
    PING = "api/ping"
    LOOKUP = "api/lookup"
    KEYWORDS = "api/keywords"
    OUT_MESSAGES = "api/out-messages"
    PREPARE_MSISDNS = "api/prepare-msisdns"
    STREX_MERCHANTS = "api/strex/merchants"

    NOT_FOUND = 404

    def __init__(self, baseUri, keyName, privateKey):
        self.client = HttpClient(baseUri, keyName, privateKey)
        self.errorHandler = HttpErrorHandler()

    # Ping controller
    def Ping(self):
        """
          Pings the service and returns a hello message
          :return: return description
        """
        response = self.client.get(self.PING)
        self.errorHandler.throwIfNotSuccess(response)
        return response.text # returns the string "pong"

    # Lookup controller

    def Lookup(self, msisdn):
        """
        Looks up address info on a mobile phone number.
        :msisdn: Mobile phone number (required)
        :return: LookupResult
        """

        if msisdn is None:
            raise ValueError("msisdn")
        payload = {"msisdn": msisdn}
        response = self.client.getWithParams(self.LOOKUP, payload)
        if response.status_code == self.NOT_FOUND:
            return None
        self.errorHandler.throwIfNotSuccess(response)
        lookupResult = LookupResult()
        lookupResult.fromDict(response.json())
        return lookupResult

    # Keyword controller

    def CreateKeyword(self, keyword):
        """
        Creates a new keyword.
        :keyword: Keyword
        :return: string
        """
        if keyword is None:
            raise ValueError("keyword")
        response = self.client.post(self.KEYWORDS, keyword)
        self.errorHandler.throwIfNotSuccess(response)

        return self._getIdFromHeader(response.headers)

    def GetAllKeywords(self, shortNumberId=None, keyword=None, mode=None, tag=None):
        """
        Gets all keywords.
        :return: Keyword[]
        """
        params = {}
        if shortNumberId is not None:
            params["shortNumberId"] = shortNumberId
        if keyword is not None:
            params["keywordText"] = keyword
        if mode is not None:
            params["mode"] = mode
        if tag is not None:
            params["tag"] = tag

        response = self.client.getWithParams(self.KEYWORDS, params)
        self.errorHandler.throwIfNotSuccess(response)
        return Keyword().fromResponseList(response.json())

    def GetKeyword(self, keywordId):
        """
        Gets a keyword.
        :keywordId: string
        :return: Keyword
        """
        if keywordId is None:
            raise ValueError("keywordId")

        response = self.client.get(self.KEYWORDS + "/" + keywordId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        
        keyword = Keyword()
        keyword.fromDict(response.json())
        return keyword

    def UpdateKeyword(self, keyword):
        """
        Updates a keywrod
        :keyword: Keyword to update      
        """
        if keyword is None:
            raise ValueError("keyword")
        if keyword.keywordId is None:
            raise ValueError("keywordId")

        response = self.client.put(
            self.KEYWORDS + "/" + keyword.keywordId, keyword)

        self.errorHandler.throwIfNotSuccess(response)

    def DeleteKeyword(self, keywordId):
        """
        Deletes a keyword
        :keywordId: string
        """
        if keywordId is None:
            raise ValueError("keywordId")

        response = self.client.delete(self.KEYWORDS + "/" + keywordId)
        self.errorHandler.throwIfNotSuccess(response)

    # OutMessage controller
    def PrepareMsisdns(self, msisdns):
        """
        MSISDNs to prepare as a string array
        :message: string[]
        """
        if msisdns is None:
            raise ValueError("msisdns")
        response = self.client.post(self.PREPARE_MSISDNS, msisdns)
        self.errorHandler.throwIfNotSuccess(response)

    def CreateOutMessage(self, message):
        """
        Creates a new out-message
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")

        response = self.client.post(self.OUT_MESSAGES, message)
        self.errorHandler.throwIfNotSuccess(response)

        return self._getIdFromHeader(response.headers)

    def CreateOutMessageBatch(self, messages):
        """
        Creates a new out-message batch.
        :messages: OutMessage[]
        """
        if messages is None:
            raise ValueError("messages")

        response = self.client.post(self.OUT_MESSAGES + "/batch", messages)
        self.errorHandler.throwIfNotSuccess(response)

    def GetOutMessage(self, transactionId):
        """
        Gets and out-message
        :transactionId: string
        :return: OutMessage
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.get(self.OUT_MESSAGES + "/" + transactionId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        outMessage = OutMessage()
        outMessage.fromDict(response.json())
        return outMessage

    def UpdateOutMessage(self, message):
        """
        Updates a future scheduled out-message.
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")
        if message.transactionId is None:
            raise ValueError("transactionId")

        response = self.client.put(
            self.OUT_MESSAGES + "/" + message.transactionId, message)
        self.errorHandler.throwIfNotSuccess(response)

    def DeleteOutMessage(self, transactionId):
        """
        Deletes a future sheduled out-message.
        :transactionId: string
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.delete(self.OUT_MESSAGES + "/" + transactionId)
        self.errorHandler.throwIfNotSuccess(response)

    def ReversePayment(self, transactionId):
        """
        NOT IN SWAGGER SPEC
        Reverses a payment transaction
        This method is idempotent and can be called multiple times without problems.
        :transactionId: string
        :return: string
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.get(
            "api/reverse-payment", params={'transactionId': transactionId})
        self.errorHandler.throwIfNotSuccess(response)
        return self._getIdFromHeader(response.headers)

    # StrexMerchantIds controller

    def GetMerchantIds(self):
        """
        Gets all merchant ids.
        :return: StrexMerchantId[]
        """
        response = self.client.get(self.STREX_MERCHANTS)
        self.errorHandler.throwIfNotSuccess(response)
        return StrexMerchantId().fromResponseList(response.json())

    def GetMerchant(self, merchantId):
        """
        Gets a merchant.
        :merchantId: string
        :returns: StrexMerchantId
        """
        if merchantId is None:
            raise ValueError("merchantId")

        response = self.client.get(self.STREX_MERCHANTS + "/" + merchantId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        strexMerchantId = StrexMerchantId()
        strexMerchantId.fromDict(response.json())
        return strexMerchantId

    def SaveMerchant(self, merchant):
        """
        Creates/updates a merchant.
        :merchant: StrexMerchantId
        """
        if merchant is None:
            raise ValueError("merchant")
        if merchant.merchantId is None:
            raise ValueError("merchantId")

        response = self.client.put(self.STREX_MERCHANTS + "/" + merchant.merchantId, merchant)
        self.errorHandler.throwIfNotSuccess(response)

    def DeleteMerchant(self, merchantId):
        """
        Deletes a merchant
        :merchantId: string
        """
        if merchantId is None:
            raise ValueError("merchantId")

        response = self.client.delete(self.STREX_MERCHANTS + "/" + merchantId)
        self.errorHandler.throwIfNotSuccess(response)
    
    def _getIdFromHeader(self, headers):
        """
        Returns the newly created resource's identifier from the Locaion header
        :returns: resource identifier
        """
        chunks = headers["Location"].split("/")
        return chunks[-1]
