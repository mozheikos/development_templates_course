"""
Module as part of business logic. Implement Ton API client
"""


from tonclient.client import TonClient, ClientConfig, MAINNET_BASE_URLS
from tonclient.types import ParamsOfQueryCollection

from schema import AccountInfo


class TonClientAPI:
    """
    Class for connect and query Everscale
    """

    def __init__(self):
        """
        Init method
        """
        self.__client = self.__get_client()

    @staticmethod
    def __get_client() -> TonClient:
        """Initialization of Ton Client"""
        config = ClientConfig()
        config.network.endpoints = MAINNET_BASE_URLS
        return TonClient(config=config)

    def get_info(self, address: str) -> AccountInfo:
        """
        Query blockchain for account information
        :param address: str
        :return: AccountInfo
        """
        response = self.__client.net.query_collection(ParamsOfQueryCollection(
            collection='accounts',
            filter={'id': {'eq': address}},
            result='id acc_type_name balance(format: DEC) code_hash data_hash'
        )).result[0]
        return AccountInfo.parse_obj(response)
