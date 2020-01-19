from urllib.request import Request, urlopen
from bs4 import BeautifulSoup



def main():
    
    arr = ['https://www.cricbuzz.com//profiles/265/ms-dhoni']
    for i in arr:
        player_dict = {
            'bio':{},
            'icc_rankings':{},
            'career':{'batting':{},'bowling':{}},
            'additional_info':{},
            'summary':{}
            }
        req = Request(i, headers = {'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        
        bsObj = BeautifulSoup(webpage, 'lxml')
        
        player_profile_obj = bsObj.find_all("div",{"id":"playerProfile"})
        generate_dict(player_profile_obj,player_dict)
        print(player_dict)
    

def generate_dict(data,player_dict):
    player_obj = player(data[0])
    player_dict['bio']['name'] = player_obj.get_player_name()
    player_dict['bio']['country'] = player_obj.get_player_country() 
    player_dict['bio']['personal_info'] = player_obj.get_personal_info(player_dict)
    
    career = player(data[0].find_all("div",{"class":"cb-player-bio"})[0].find_all("div"))
    player_dict['career']['batting'] = career.get_batting_career()
    player_dict['career']['bowling'] = career.get_bowling_career()
    player_dict['additional_info'] = career.get_additional_career_info()
    
    player_dict['summary'] = data[0].find_all("div",{"class":"cb-player-bio"})[1].get_text()

    
    
    
class player:
    
    def __init__(self,data):
        self.data = data
    
    def get_player_name(self):
        name = self.data.find("h1").get_text()
        return name

    def get_player_country(self):
        country = self.data.find("h3").get_text()
        return country    

    def get_personal_info(self,player_dict):
        personal_info_dict = {}
        container = self.data.find("div",{"class":"cb-hm-rght"}).find_all("div")
        
        for i in range(1,len(container),2):
            if(container[i].get_text().strip() == 'ICC Rankings'):
                player_dict['icc_rankings'] = player.get_player_rankings(container,i+2)
                break;
            else:
                personal_info_dict[container[i].get_text().strip()] = container[i+1].get_text().split("(")[0].strip()
        player.get_player_teams(container[len(container)-1],player_dict)
        return(personal_info_dict)
    
    def get_player_rankings(container,index):
        ranking_dic = {'batting':{},'bowling':{}}
        for i in range(index,len(container)-4,):
            if(i >= index and i<=index+2):
                ranking_dic['batting'][container[i].get_text().strip()] = container[i+4].get_text().strip()
            elif(i >= index+3 and i<=index+4):
                continue
            elif(i>index+4 and i<=index+7):
                ranking_dic['bowling'][container[i-5].get_text().strip()] = container[i+3].get_text().strip()
            else:
                break
        return ranking_dic

    def get_player_teams(data,player_dict):
        player_dict['bio']['teams'] = data.get_text()


    def get_batting_career(self):
        container = self.data[1].find("table").find_all("tr")
        batting_career = {'test':{},'odi':{},'t20':{},'ipl':{},}
        
        labels = ['matches','innings','not_out','runs','highest','average','balls_faced','strike_rate','100','200','50','4','6']
        
        for i in range(1,len(container)):
            row_data = container[i].find_all("td")
            match_format = row_data[0].get_text()
            if match_format == "Test":
                for ind,val in enumerate(labels):
                    batting_career["test"][val] = row_data[ind+1].get_text()
            if match_format == "ODI":
                for ind,val in enumerate(labels):
                    batting_career["odi"][val] = row_data[ind+1].get_text()
            if match_format == "T20I":
                for ind,val in enumerate(labels):
                    batting_career["t20"][val] = row_data[ind+1].get_text()
            if match_format == "IPL":
                for ind,val in enumerate(labels):
                    batting_career["ipl"][val] = row_data[ind+1].get_text()
                
        return batting_career
    
    def get_bowling_career(self):
        container = self.data[3].find("table").find_all("tr")
        bowling_career = {'test':{},'odi':{},'t20':{},'ipl':{},}
        
        labels = ['matches','innings','balls','runs','wickets','best_in_innings','best_in_match','economy','average','strike_rate','5W','10W']
        
        for i in range(1,len(container)):
            row_data = container[i].find_all("td")
            match_format = row_data[0].get_text()
            if match_format == "Test":
                for ind,val in enumerate(labels):
                    bowling_career["test"][val] = row_data[ind+1].get_text()
            if match_format == "ODI":
                for ind,val in enumerate(labels):
                    bowling_career["odi"][val] = row_data[ind+1].get_text()
            if match_format == "T20I":
                for ind,val in enumerate(labels):
                    bowling_career["t20"][val] = row_data[ind+1].get_text()
            if match_format == "IPL":
                for ind,val in enumerate(labels):
                    bowling_career["ipl"][val] = row_data[ind+1].get_text()
        
        return bowling_career

    def get_additional_career_info(self):
        additional_info = {}
        container = self.data[6].find_all("div")
        for i in range (0,len(container),2):
            additional_info[container[i].get_text().strip()] = container[i+1].get_text().strip()
        return additional_info    
        
    
if __name__ == '__main__':
    main()