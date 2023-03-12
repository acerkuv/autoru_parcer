from os import path, listdir
import datetime, json
# import pandas as pd
 
wd = path.join(path.dirname(__file__), 'excel')
cards_dir = path.join(path.dirname(__file__), 'cards')
 
card_files = listdir(cards_dir)
 
all_cars = {}
 
with open(path.join(wd, 'report.csv'), 'w') as f:
 
    f.write(';'.join([
        'number',
        'model_name',
        'year', 
        'equipment',
        'status',
        'max_price',
        'min_price',
        'max_discount',
        'VAT',
        'dealership_name',
        'dealership_city',
        'disqount_dict', '\n']))
 
    for json_f in card_files[:]:
        with open(path.join(cards_dir, json_f), 'r') as mf:
            for line in mf:
                temp = json.loads(line)
                tj = json.loads(temp)
                cdata = []
                for key in tj.keys():
                    cdata.append(str(tj.get(key)))
                    
                f.write(';'.join(cdata) + '\n')
                
            mf.close()
    f.close()