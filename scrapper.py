#HI There
from urllib.request import Request, urlopen, URLopener
from bs4 import BeautifulSoup
import html
import json
import sys
sys.path.append('D:\\Python Scrapping Project')
import winnersXLS
from commonFunctions import commonFunctions,excel_file, write_match_info

scorecard_root_class = "cb-ltst-wgt-hdr"
scorecard_items_class = "cb-scrd-itms"
batting_index = 0
bowling_index = 1
    

def main2():
   opener = URLopener()
   opener.addheader('User-Agent', 'Mozilla/5.0')
   filename, headers = opener.retrieve('https://www.cricbuzz.com/a/img/v1/152x152/i1/c170677/ms-dhoni.jpg', 'Test.jpg')
    
    
def main():
    winner_workbook = excel_file.init_workbook()
    winner_worksheet = excel_file.init_worksheet(winner_workbook,'winnerXLS')
    match_info_workbook = excel_file.init_workbook()
    match_info_worksheet = excel_file.init_worksheet(match_info_workbook,'match_info_XLS')
    f = open("D:\\Python Scrapping Project\\files\\logs\\error_updated_6000_7000.txt","a")
    player = open("D:\\Python Scrapping Project\\files\\player\\player_profile_updated_6000_7000.txt","a")
    
    ind = 1
    for main_index in range (6000,7000):
        req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/"+str(main_index) , headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
    
        bsObj = BeautifulSoup(webpage, 'lxml')
        
        try:
            winner_dic = winnersXLS.find_winner(main_index,bsObj,winner_worksheet,ind)
            write_match_info.write(main_index,bsObj,match_info_worksheet,ind)
            ind = ind +1
            if(commonFunctions.find_match_type(bsObj) == 'Test'):
                match_dict = commonFunctions.generate_match_dict('Test',main_index,winner_dic)
            elif(commonFunctions.find_match_type(bsObj) == 'One-Day'):
                match_dict = commonFunctions.generate_match_dict('One-Day',main_index,winner_dic)
            create_match_json(bsObj,match_dict,player)
            with open('D:\\Python Scrapping Project\\files\\match json\\data'+str(main_index)+'.json','w') as outfile:
                json.dump(match_dict,outfile)
            print("Successful for index: " + str(main_index))
        except:
            match_dict = commonFunctions.generate_match_dict('empty',main_index,winner_dic)
            commonFunctions.writeToLog(f,"Error for index: " + str(main_index))
            print("Error for index: " + str(main_index))
        #print("Match DATA for index -------------->"+str(main_index))
        #print(match_dict)
            
    excel_file.save_excelfile(winner_workbook,'winnerXLS')
    excel_file.save_excelfile(match_info_workbook,'match_info_XLS')
    f.close()
    player.close()
    
    
def create_match_json(data,match_dict,player):    
    matchInfo.match_info(data,match_dict)
    matchData.match_scores_json(data,match_dict,player)
    matchInfo.playing_XI(data,match_dict,player)

class matchData:
    
    def batsman_data(scorecard_items,innings,match_dict,player):
        batsman_dict = {}
        labels = ['name','result','runs','balls','4','6','SR','link']
        end_index = commonFunctions.find_end_index(scorecard_items)
        for i in range(0,end_index):
            inner_dict = dict.fromkeys(labels,'')
            batsman = scorecard_items[i].find_all("div")
            #commonFunctions.write_to_profile(batsman,player)
            
            for ind,val in enumerate(labels):
                if val == 'link':
                    inner_dict[val] = batsman[0].find("a")['href'].strip()
                else:
                    inner_dict[val] = batsman[ind].get_text().strip()
            batsman_dict[i] = inner_dict
        match_dict['match_scores'][innings]['batting_data'] = batsman_dict
    
    
    def bowlers_data(scorecard_items,innings,match_dict,player):
        bowler_dict = {}
        labels = ['name','overs','maiden','runs','wickets','no_balls','wides','economy','link']
        for i in range(0,len(scorecard_items)):
            inner_dict = dict.fromkeys(labels,'')
            bowler = scorecard_items[i].find_all("div")
            #commonFunctions.write_to_profile(bowler,player)
            for ind,val in enumerate(labels):
                if val == 'link':
                    inner_dict[val] = bowler[0].find("a")['href'].strip()
                else:
                    inner_dict[val] = bowler[ind].get_text().strip()
            bowler_dict[i] = inner_dict
        match_dict['match_scores'][innings]['bowling_data'] = bowler_dict
        
    
    def match_scores_json(data,match_dict,player):
        if(commonFunctions.find_match_type(data) == 'Test'):
            innings_array = ['innings_1','innings_2','innings_3','innings_4']
        else:
            innings_array = ['innings_1','innings_2']
        for i in innings_array:
            if(commonFunctions.if_proceed(data,i)):
                batting_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[batting_index].find_all("div",{"class":scorecard_items_class})
                bowling_items = data.find("div",{"id":i}).find_all("div",{"class":scorecard_root_class})[bowling_index].find_all("div",{"class":scorecard_items_class})
                matchData.batsman_data(batting_items,i,match_dict,player)
                matchData.bowlers_data(bowling_items,i,match_dict,player)
            else:
                match_dict['match_scores'][i]['batting_data'] = {}
                match_dict['match_scores'][i]['bowling_data'] = {}
        return
    
class matchInfo:
    
    def playing_XI(data,match_dict,player):
        container = data.find_all("div",{"class","cb-minfo-tm-nm"})
        #squad = {'team_1':{},'team_2':{}}
        inner_dict = {}
        if(len(container)>4):
            sub_container_team_1 = container[2].find_all("a")
            sub_container_team_2 = container[5].find_all("a")
            for i in range(len(sub_container_team_1)):
                player_dict = {'name':'','link':''}
                player_dict['name'] = sub_container_team_1[i].get_text()
                player_dict['link'] = sub_container_team_1[i]['href']
                commonFunctions.write_to_profile(player_dict,player)
                inner_dict[i] = player_dict
            match_dict['squad']['team_1'] = inner_dict
            
            for i in range(len(sub_container_team_2)):
                player_dict = {'name':'','link':''}
                player_dict['name'] = sub_container_team_2[i].get_text()
                player_dict['link'] = sub_container_team_2[i]['href']
                commonFunctions.write_to_profile(player_dict,player)
                inner_dict[i] = player_dict
            match_dict['squad']['team_2'] = inner_dict
        
        else:
            sub_container_team_1 = container[1].find_all("a")
            sub_container_team_2 = container[3].find_all("a")
            for i in range(len(sub_container_team_1)):
                player_dict = {'name':'','link':''}
                player_dict['name'] = sub_container_team_1[i].get_text().strip()
                player_dict['link'] = sub_container_team_1[i]['href'].strip()
                commonFunctions.write_to_profile(player_dict,player)
                inner_dict[i] = player_dict
            match_dict['squad']['team_1'] = inner_dict
        
            for i in range(len(sub_container_team_2)):
                player_dict = {'name':'','link':''}
                player_dict['name'] = sub_container_team_2[i].get_text()
                player_dict['link'] = sub_container_team_2[i]['href']
                commonFunctions.write_to_profile(player_dict,player)
                inner_dict[i] = player_dict
            match_dict['squad']['team_2'] = inner_dict
    
    def match_info(data,match_dict):
        info_points = data.find_all("div",{"class":"cb-mtch-info-itm"})
        #print(len(info_points))
        info_labels=[]
        info_data = []
        for i in range(len(info_points)):
            info_labels.append(info_points[i].find_all("div")[0].get_text().strip())
            info_data.append(html.unescape(info_points[i].find_all("div")[1].get_text().strip()))
        
        match_dict['match_info'] = dict.fromkeys(info_labels,'')
        for ind,val in enumerate(info_labels):
            match_dict['match_info'][val] = info_data[ind].strip()
        
        control_type = 'match_details'
        info_string = info_data[info_labels.index('Match')]
        matchInfo.additional_info(control_type,info_string,match_dict)
        if(commonFunctions.find_match_type(data) == 'Test'):
            match_dict['match_info']['format'] = 'Test'
        else:
            match_dict['match_info']['format'] = 'limited-over'
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
