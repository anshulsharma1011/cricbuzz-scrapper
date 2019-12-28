from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
#import json

match_dict = {
        'match_info':{},
        'match_scores':{
                'innings_1':{},
                'innings_2':{}
                }
        }

scorecard_root_class = "cb-ltst-wgt-hdr"
scorecard_items_class = "cb-scrd-itms"
batting_index = 0
bowling_index = 1

def test():
    req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/3042", headers = {'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    bsObj = BeautifulSoup(webpage, 'lxml')
    first_innings = bsObj.find("div",{"id":"innings_2"})
    print(first_innings==None)
    
    
    
    
def main():
    for main_index in range (3000,3001):
        req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/"+str(main_index) , headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
    
        bsObj = BeautifulSoup(webpage, 'lxml')
        create_match_json(bsObj)
        print("Match DATA for index -------------->"+str(main_index))
        print(match_dict)
        #with open('D:\\Python Scrapping Project\\JSON DATA\\data'+str(main_index)+'.json','w') as outfile:
            #json.dump(match_dict,outfile)

def find_end_index(batting_items):
    end_index = len(batting_items)
    last_value = batting_items[end_index-1].get_text().strip()[0:3]
    if(last_value == 'Did'):
            end_index = len(batting_items)-3
    else:
        end_index = len(batting_items)-2
    return end_index
    
    
def create_match_json(data):    
    match_info(data)
    #match_scores_json(data)
    

def if_proceed(data,innings):
    first_innings = data.find("div",{"id":innings})
    if(first_innings != None):
        return True
    else:
        return False
    

def match_info(data):
    match_info = data.find_all("div",{"class":"cb-mtch-info-itm"})[1].find_all("div")
    print(match_info[1])

def match_scores_json(data):
    innings_array = ['innings_1','innings_2']
    for i in innings_array:
        if(if_proceed(data,i)):
            batting_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[batting_index].find_all("div",{"class":scorecard_items_class})
            bowling_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[bowling_index].find_all("div",{"class":scorecard_items_class})
            batsman_data(batting_items,i)
            bowlers_data(bowling_items,i)
        else:
            match_dict['match_scores'][i]['batting_data'] = {}
            match_dict['match_scores'][i]['bowling_data'] = {}
    return

def bowlers_data(scorecard_items,innings):
    bowler_dict = {}
    labels = ['name','overs','maiden','runs','wickets','no_balls','wides','economy']
    for i in range(0,len(scorecard_items)):
        inner_dict = dict.fromkeys(labels,'')
        bowler = scorecard_items[i].find_all("div")
        for ind,val in enumerate(labels):
            inner_dict[val] = bowler[ind].get_text()
        bowler_dict[i] = inner_dict
    match_dict['match_scores'][innings]['bowling_data'] = bowler_dict


def batsman_data(scorecard_items,innings):
    batsman_dict = {}
    labels = ['name','result','runs','balls','4','6','SR']
    end_index = find_end_index(scorecard_items)
    for i in range(0,end_index):
        inner_dict = dict.fromkeys(labels,'')
        batsman = scorecard_items[i].find_all("div")
        
        for ind,val in enumerate(labels):
            inner_dict[val] = batsman[ind].get_text()
        batsman_dict[i] = inner_dict
    match_dict['match_scores'][innings]['batting_data'] = batsman_dict

if __name__ == '__main__':
    main()
