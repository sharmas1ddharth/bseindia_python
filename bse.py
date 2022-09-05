import urllib.request
import pandas as pd
import json

class BSE:
  def __init__(self,start_date:str, end_date:str, code:list, csv=False, show=False) -> None:
    self.start_date = start_date
    self.end_date = end_date
    self.code = code
    self.csv = csv
    self.show = show

  def make_csv(self, data:json) -> None:
    df = pd.DataFrame(columns = ['Date','Open', 'High', 'Low', 'Close'])
    name = data['scrip_id']
    stockdata = data['StockData']
    for d in stockdata:
      temp = []
      temp.append(d['Dates'])
      temp.append(d['qe_open'])
      temp.append(d['qe_high'])
      temp.append(d['qe_low'])
      temp.append(d['qe_close'])

      df.loc[len(df.index)] = temp
    df.set_index(['Date'], inplace = True)
    df.to_csv(f'{name}.csv')

  def fetch(self) -> json:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    headers = {'User-Agent' : user_agent}
    
    for c in self.code:
      url= f'https://api.bseindia.com/BseIndiaAPI/api/StockpricesearchData/w?MonthDate={self.start_date}&Scode={c}&YearDate={self.end_date}&pageType=0&rbType=D'
      req = urllib.request.Request(url, None, headers)

      content = urllib.request.urlopen(req)
      s = content.read().decode('utf-8')

      data = json.loads(s)

      if self.csv == True:
        self.make_csv(data)
        print(f"{data['scrip_id']} csv file Generated")
        
        if self.show == True:
          return data

      else:
        return data
    # name = make_csv(data)
    # stock_names.append(name)
    # print("--------------------------------------------------------------------------")
    # 