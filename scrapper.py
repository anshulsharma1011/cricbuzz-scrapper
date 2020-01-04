#HI There
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import html
#import json



scorecard_root_class = "cb-ltst-wgt-hdr"
scorecard_items_class = "cb-scrd-itms"
batting_index = 0
bowling_index = 1

def main2():
    req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/22583", headers = {'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    bsObj = BeautifulSoup(webpage, 'lxml')
    print(bsObj)
    text = "B Oxenford,&nbsp;R Tucker"
    print(html.unescape(text))
    
    
    
    
def main():
    for main_index in range (22582,22583):
        req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/"+str(main_index) , headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
    
        bsObj = BeautifulSoup(webpage, 'lxml')
        #date = bsObj.find_all("div",{"class":"cb-mtch-info-itm"})[1].get_text()
        #print(date + str(main_index))
        if(find_match_type(bsObj) == 'Test'):
            match_dict = {'match_result':{'winner':'','description':''},'match_info':{},'match_scores':{'innings_1':{},'innings_2':{},'innings_3':{},'innings_4':{}}}
        else:
            match_dict = {'match_result':{'winner':'','description':''},'match_info':{},'match_scores':{'innings_1':{},'innings_2':{}}}
        create_match_json(bsObj,match_dict)
        print("Match DATA for index -------------->"+str(main_index))
        print(match_dict)
        #with open('D:\\Python Scrapping Project\\JSON DATA\\data'+str(main_index)+'.json','w') as outfile:
            #json.dump(match_dict,outfile)

def find_end_index(batting_items):
    end_index = len(batting_items)
    last_value = batting_items[end_index-1].get_text().strip()[0:3]
    if(last_value == 'Did' or last_value == 'Yet'):
            end_index = len(batting_items)-3
    else:
        end_index = len(batting_items)-2
    return end_index
    
    
def create_match_json(data,match_dict):    
    match_info(data,match_dict)
    #match_scores_json(data,match_dict)
    match_result(data,match_dict)

def if_proceed(data,innings):
    find_innings = data.find("div",{"id":innings})
    if(find_innings != None):
        return True
    else:
        return False

def find_match_type(data):
    match_date = data.find_all("div",{"class":"cb-mtch-info-itm"})[1].get_text().split()
    if("-" in match_date):
        match_type = "Test"
    else:
        match_type = "One-Day"
    return match_type

def match_info(data,match_dict):
    info_points = data.find_all("div",{"class":"cb-mtch-info-itm"})
    #print(len(info_points))
    info_labels=[]
    info_data = []
    for i in range(len(info_points)):
        info_labels.append(info_points[i].find_all("div")[0].get_text())
        info_data.append(html.unescape(info_points[i].find_all("div")[1].get_text()))
    
    match_dict['match_info'] = dict.fromkeys(info_labels,'')
    for ind,val in enumerate(info_labels):
        match_dict['match_info'][val] = info_data[ind]
    
    control_type = 'match_details'
    info_string = info_data[info_labels.index('Match')]
    additional_info(control_type,info_string,match_dict)
    return
    

def match_scores_json(data,match_dict):
    if(find_match_type(data) == 'Test'):
        innings_array = ['innings_1','innings_2','innings_3','innings_4']
    else:
        innings_array = ['innings_1','innings_2']
    for i in innings_array:
        if(if_proceed(data,i)):
            batting_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[batting_index].find_all("div",{"class":scorecard_items_class})
            bowling_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[bowling_index].find_all("div",{"class":scorecard_items_class})
            batsman_data(batting_items,i,match_dict)
            bowlers_data(bowling_items,i,match_dict)
        else:
            match_dict['match_scores'][i]['batting_data'] = {}
            match_dict['match_scores'][i]['bowling_data'] = {}
    return

def bowlers_data(scorecard_items,innings,match_dict):
    bowler_dict = {}
    labels = ['name','overs','maiden','runs','wickets','no_balls','wides','economy']
    for i in range(0,len(scorecard_items)):
        inner_dict = dict.fromkeys(labels,'')
        bowler = scorecard_items[i].find_all("div")
        for ind,val in enumerate(labels):
            inner_dict[val] = bowler[ind].get_text()
        bowler_dict[i] = inner_dict
    match_dict['match_scores'][innings]['bowling_data'] = bowler_dict


def batsman_data(scorecard_items,innings,match_dict):
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


def match_result(data,match_dict):
    result = data.find_all("div",{"class":"cb-text-complete"})[0].get_text()
    match_dict['match_result']['description'] = result
    return


def additional_info(control,info,match_dict):
    if(control == 'match_details'):
        info = info.split(",")
        team_1 = info[0].split("vs")[0]
        team_2 = info[0].split("vs")[1]
        match_dict['match_info']['team_1'] = team_1
        match_dict['match_info']['team_2'] = team_2
        
    return

if __name__ == '__main__':
    main()
