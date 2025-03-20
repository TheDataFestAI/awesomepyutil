""" 
1. py tasks\stock_market_data_tasks\nse_stock_market.py
"""

import os, sys
import pandas as pd
import requests

# parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
# sys.path.append(parentdir)

niftyTypes = ["NIFTY 50", "NIFTY NEXT 50", "NIFTY MIDCAP SELECT", "NIFTY BANK", "NIFTY FINANCIAL SERVICES"]
nifty_legends = [['NIFTY', 'NIFTY 50'], ['BANKNIFTY', 'BANK NIFTY'], ['NIFTYNEXT50', 'NIFTY NEXT 50'], ['SecGtr20', 'Securities > Rs 20'], ['SecLwr20', 'Securities < Rs 20'], ['FOSec', 'F&O Securities'], ['allSec', 'All Securities']] 
monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class NSE():
    # setup nse headers
    nse_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Accept-Language': 'en,gu;q=0.9,hi;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'accept-encoding': 'gzip, deflate, br'
    }
    
    # lists of nse apis
    nse_apis = {
        "nse_base_url": "https://www.nseindia.com",
        "company_meta_info_url": "https://www.nseindia.com/api/equity-meta-info?symbol={}",
        # "allsec_gainers": "/api/liveanalysis/gainers/allSec",
        # "allsec_loosers": "/api/liveanalysis/loosers/allSec",
        "index_gainers": "/api/live-analysis-variations?index=gainers",
        "index_loosers": "/api/live-analysis-variations?index=loosers",
        "nse_etf": "/api/etf",
        "allcontracts": "api/equity-stock?index=allcontracts",
        "nifty50_daily": "/api/marketStatus",
        "test": "/api/search/autocomplete"
    }
    
    index_gainers_loosers_col = ["symbol", "ltp", "prev_price", "open_price", "high_price", "low_price", "trade_quantity", "series", "net_price", "turnover", "market_type", "ca_ex_dt", "ca_purpose", "perChange"]
    
    
    # setup nse sessions to call nse apis
    def __init__(self):
        self.session = requests.Session()
        self.request = self.session.get(self.nse_apis["nse_base_url"], headers=self.nse_headers, timeout=5)
        self.cookies = dict(self.request.cookies)
        
    def company_meta_details(company_symbol: str) -> dict:
        url = nse_company_meta_info_url.format(company_symbol)
        
        session = requests.Session()
        request = session.get(nse_base_url, headers=headers, timeout=5)
        cookies = dict(request.cookies)
        response = session.get(url, headers=headers, timeout=5, cookies=cookies)
        out = response.json()
        return out
    
    def get_marketstate_daily(self):
        url = self.nse_apis["nse_base_url"] + self.nse_apis["nifty50_daily"]
        response = self.session.get(url, headers=self.nse_headers, timeout=5, cookies=self.cookies)
        if response.status_code == 200:
            # out_df = pd.DataFrame(response.json().get("marketcap"))
            out_df = pd.DataFrame(response.json().get("marketState"))
            out_df = out_df.loc[out_df["market"].isin(["Capital Market", "currencyfuture"]), ["market", "tradeDate", \
                                                                                              "last", "variation", \
                                                                                              "percentChange"]]
            return out_df
        else:
            return {"error": "Failed to fetch data"}
    
    # get nse index gainer
    def get_index_gainers(self) -> dict:
        url = self.nse_apis["nse_base_url"] + self.nse_apis["index_gainers"]
        response = self.session.get(url, headers=self.nse_headers, timeout=5, cookies=self.cookies)
        if response.status_code == 200:
            index_gainers = response.json()
            index_gainers_legends_unique = list()
            index_gainers_legends_details = dict()
            for i in index_gainers.get("legends"):
                index_gainers_legends_unique.append(i[0])
                index_gainers_legends_details[i[0]] = i[1]
            index_gainers_list_df = list()
            for i in index_gainers_legends_unique:
                # print(f"{i=}")
                # print(f'{len(index_loosers.get(i).get("data"))=}')
                if len(index_gainers.get(i).get("data")) == 0:
                    continue     
                df = (pd.DataFrame(index_gainers.get(i).get("data"))).loc[:, self.index_gainers_loosers_col]
                df.insert(loc=0, column="index_type", value="index - " + i)
                df.insert(loc=2, column="as_of_date", value=index_gainers.get(i).get("timestamp"))
                df.insert(loc=0, column="gain_loss", value="gain")
                index_gainers_list_df.append(df)
            index_gainers_df = pd.concat(index_gainers_list_df, axis=0)
            # print(f"size of gainers data: {index_gainers_df.shape}")
            # print(f"gain or loass: {index_gainers_df["gain_loss"].unique()}")
            
            index_gainers_df["frm_prevday_gapup%"] = round(((index_gainers_df["open_price"] - index_gainers_df["prev_price"]) / index_gainers_df["prev_price"]) * 100, 2)
            index_gainers_df["frm_prevday_gain%"] = round(((index_gainers_df["ltp"] - index_gainers_df["prev_price"]) / index_gainers_df["prev_price"]) * 100, 2)
        
            return index_gainers_df
        else:
            return {"error": "Failed to fetch data"}
    
    # get nse index looser
    def get_index_loosers(self) -> dict:
        url = self.nse_apis["nse_base_url"] + self.nse_apis["index_loosers"]
        response = self.session.get(url, headers=self.nse_headers, timeout=5, cookies=self.cookies)
        if response.status_code == 200:
            index_loosers = response.json()
            index_loosers_legends_unique = list()
            index_loosers_legends_details = dict()
            for i in index_loosers.get("legends"):
                index_loosers_legends_unique.append(i[0])
                index_loosers_legends_details[i[0]] = i[1]
            index_loosers_list_df = list()
            for i in index_loosers_legends_unique:
                # print(f"{i=}")
                # print(f'{len(index_loosers.get(i).get("data"))=}')
                if len(index_loosers.get(i).get("data")) == 0:
                    continue
                df = (pd.DataFrame(index_loosers.get(i).get("data"))).loc[:, self.index_gainers_loosers_col]
                df.insert(loc=0, column="index_type", value="index - " + i)
                df.insert(loc=2, column="as_of_date", value=index_loosers.get(i).get("timestamp"))
                df.insert(loc=0, column="gain_loss", value="loss")
                index_loosers_list_df.append(df)
            index_loosers_df = pd.concat(index_loosers_list_df, axis=0)
            # print(f"size of loosers data: {index_loosers_df.shape}")
            # print(f"gain or loass: {index_loosers_df["gain_loss"].unique()}")
            
            index_loosers_df["frm_prevday_gapup%"] = round(((index_loosers_df["open_price"] - index_loosers_df["prev_price"]) / index_loosers_df["prev_price"]) * 100, 2)
            index_loosers_df["frm_prevday_gain%"] = round(((index_loosers_df["ltp"] - index_loosers_df["prev_price"]) / index_loosers_df["prev_price"]) * 100, 2)
            return index_loosers_df
        else:
            return {"error": "Failed to fetch data"}
        
    def _get_fii_data(self) -> dict:
        return 1

    
    
def get_company_current_stock_price(company_symbol: str) -> dict:
    # https://www.nseindia.com/api/quote-equity?symbol=SANGHVIMOV
    return 1


if __name__ == "__main__":
    # company_list = ["SANGHVIMOV"]
    # for i in company_list:
    #     out = company_meta_details(i)
    #     print(out)
    nse = NSE()
    
    out = nse.get_index_gainers()
    print(f"{out}")
    
    out = nse.get_index_loosers()
    print(f"{out}")
    
    out = nse.get_marketstate_daily()
    print(f"{out}")
    
    
