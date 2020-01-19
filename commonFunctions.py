import xlwt


class commonFunctions:

    def writeToLog(file,string):
        file.write(string)
        file.write("\n")
        file.write("\n")
        return
    
    def generate_match_dict(dict_type,main_index,winner_dic = None):
        if(dict_type == 'Test'):
            match_dict = {'match_index':main_index,'match_result':winner_dic,'match_info':{},'squad':{'team_1':{},'team_2':{}},'match_scores':{'innings_1':{},'innings_2':{},'innings_3':{},'innings_4':{}}}
        elif(dict_type == 'One-Day'):
            match_dict = {'match_index':main_index,'match_result':winner_dic,'match_info':{},'squad':{'team_1':{},'team_2':{}},'match_scores':{'innings_1':{},'innings_2':{}}}
        elif(dict_type == 'empty'):
            match_dict = {'match_index':main_index,'match_result':{},'match_info':{},'squad':{},'match_scores':{'innings_1':{},'innings_2':{}}}
            
        return match_dict
        
    def find_match_type(data):
        match_date = data.find_all("div",{"class":"cb-mtch-info-itm"})[1].get_text().split()
        if("-" in match_date):
            match_type = "Test"
        else:
            match_type = "One-Day"
        return match_type
    
    def if_proceed(data,innings):
        find_innings = data.find("div",{"id":innings})
        if(find_innings != None):
            return True
        else:
            return False


    def find_end_index(batting_items):
        end_index = len(batting_items)
        last_value = batting_items[end_index-1].get_text().strip()[0:3]
        if(last_value == 'Did' or last_value == 'Yet'):
                end_index = len(batting_items)-3
        else:
            end_index = len(batting_items)-2
        return end_index
    
    
    def write_to_profile(container,file):
        name = container['name']
        link = container['link']
        file.write(name + ' : ' + link)
        file.write("\n")

        return
    
class excel_file:
    def init_workbook():
        workbook = xlwt.Workbook(encoding = 'ascii')
        return workbook
    
    def init_worksheet(workbook,controlId):
        if(controlId == 'winnerXLS'):    
            worksheet = workbook.add_sheet('Winners Data')
            worksheet.write(0, 0, label = 'Match Index')
            worksheet.write(0, 1, label = 'Result Description')
            worksheet.write(0, 2, label = 'Result')
            worksheet.write(0, 3, label = 'Winner')
            worksheet.write(0, 4, label = 'Special Case')
        elif(controlId == 'match_info_XLS'):
            worksheet = workbook.add_sheet('Winners Data')
            worksheet.write(0, 0, label = 'Match Index')
            worksheet.write(0, 1, label = 'Match Title')
            worksheet.write(0, 2, label = 'Match Date')
        return worksheet
    
    def save_excelfile(workbook,controlId):
        if(controlId == 'winnerXLS'):
            workbook.save('D:\\Python Scrapping Project\\files\\excel\\winnersTest_updated_6000_7000.xls')
        elif(controlId == 'match_info_XLS'):
            workbook.save('D:\\Python Scrapping Project\\files\\excel\\match_info_updated_6000_7000.xls')


class write_match_info:
    def write(main_index,data,worksheet,ind):
        try:
            info_points = data.find_all("div",{"class":"cb-mtch-info-itm"})
            title = info_points[0].find_all("div")[1].get_text().strip()
            date = info_points[1].find_all("div")[1].get_text().strip()
            worksheet.write(ind, 0, label = main_index)
            worksheet.write(ind, 1, label = title)
            worksheet.write(ind, 2, label = date)
        except:
            pass
        
        
        return