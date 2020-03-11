import json
import pprint

DATA_PATH = "crawled_data.json"

if __name__ == "__main__":
    with open(DATA_PATH) as json_file:
        json_list = json.load(json_file)
        # pprint.pprint(finance_list[0])
        dsr = json_list[0]
        pprint.pprint(dsr)
        for finance in dsr['finance']:
          bps = finance['bps']
          print(bps)
          bps = int(bps.replace(',', ''))
          print(str(bps))

          
