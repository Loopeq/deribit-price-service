import aiohttp


class MarketDataClient:
    API_URL = "https://deribit.com/api/v2"

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def get_index_price(self, ticker: str) -> float:

        url = f"{self.API_URL}/public/get_index_price"
        params = {"index_name": ticker}

        async with self._session.get(url=url, params=params) as response:
            response.raise_for_status()
            data = await response.json()

        result = data.get("result")

        if not result:
            raise Exception('Field "result" is missing')

        price = result.get("index_price")

        if not price:
            raise Exception('Field "price" is missing')

        return price
