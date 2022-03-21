import json

import scrapy
from ..items import StockDetails

class Stocklist(scrapy.Spider):
    name = "getall"

    start_urls = [
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=A',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=B',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=C',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=D',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=E',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=F',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=G',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=H',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=I',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=J',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=K',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=L',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=M',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=N',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=O',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=P',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=Q',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=R',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=S',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=T',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=U',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=V',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=W',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=X',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=Y',
        'https://frapi.marketsmojo.com/stocks_Footer/get_stocks?alphabet=Z'
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        for data in jsonresponse["data"]:
            stockitem = StockDetails()

            stockId = self.F_GetData(data, "Id")
            stockId = str(stockId)
            stockitem["id"] = stockId

            companyName = self.F_GetData(data, "Company")
            companyName = str(companyName)
            stockitem["companyName"] = companyName
            
            if (stockId and stockId.strip()):
                priceUrl = 'https://frapi.marketsmojo.com/stocks_stocksid/header_info?sid=' + str(stockId) + '&exchange=undefined'
                yield scrapy.Request(priceUrl, callback=self.parse_stock_price, cb_kwargs=dict(stockitem=stockitem))
               
    def parse_stock_price(self, response, stockitem):
        jsonresponse = json.loads(response.text)
        if jsonresponse["code"] == "200":
            jsondata = jsonresponse["data"]
            try:
                stockitem["price"] = jsondata["stock"]["price"]["value"]
            except:
                stockitem["price"] = ""

            detailsUrl = 'https://frapi.marketsmojo.com/stocks_dashboard/stockinfo?sid=' + stockitem["id"] +'&callback=?'
            yield scrapy.Request(detailsUrl, callback=self.parse_stock_details, cb_kwargs=dict(stockitem=stockitem))

    def parse_stock_details(self, response, stockitem):
        jsonresponse = json.loads(response.text)
        if jsonresponse["code"] == 200:
            jsondata = jsonresponse["data"]
            try:
                stockitem["valuation"] = jsondata["valuation"]["status"]
            except:
                stockitem["valuation"] = ""
            
            try:
                stockitem["quality"] = jsondata["quality"]["status"] 
            except:
                stockitem["quality"] = ""
            
            try:
                stockitem["technicals"] = jsondata["technicals"]["status"]
            except:
                stockitem["technicals"] = ""
            
            try:
                stockitem["fintrend"] = jsondata["fintrend"]["status"]
            except:
                stockitem["fintrend"] = ""

            scoreUrl = 'https://frapi.marketsmojo.com/stocks_Stocksid/returnContri_info?sid=' + str(
                stockitem["id"]) + '&stockID=' + stockitem["id"] + '&exchange=0&'
            yield scrapy.Request(scoreUrl, callback=self.parse_stock_score, cb_kwargs=dict(stockitem=stockitem))

    def parse_stock_score(self, response, stockitem):
        jsonresponse = json.loads(response.text)
        if jsonresponse["code"] == "200":
            jsondata = jsonresponse["data"]
            try:
                stockitem["value"] = jsondata["score"]["value"]
            except:
                stockitem["value"] = ""
            
            try:
                stockitem["call_type"] = jsondata["score"]["call_type"]
            except:
                stockitem["call_type"] = ""
                
            yield stockitem

    def F_GetData(self, p_data, p_key):
        try:
            return p_data[p_key]
        except (KeyError, AttributeError):
            return ''