import sys
import json
import xlwt
sys.path.append('D:\\Python Scrapping Project')

workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('playerProfileLink')
worksheet.write(0, 0, label = 'S NO')
worksheet.write(0, 1, label = 'Player Name')
worksheet.write(0, 2, label = 'Player Link')
worksheet.write(0, 3, label = 'Name TAG1')
worksheet.write(0, 4, label = 'Name TAG2')
worksheet.write(0, 5, label = 'Name TAG3')
worksheet.write(0, 6, label = 'Name TAG4')
worksheet.write(0, 7, label = 'Name TAG5')
worksheet.write(0, 8, label = 'Name TAG6')
worksheet.write(0, 9, label = 'Name TAG7')

file_name = "player_profile_updated_12000_3"
f = open("D:\\Python Scrapping Project\\files\\player\\"+file_name+".txt", "r")

playerDictionary = {}

arr = list(set(f))
for i,l in enumerate(arr):
    inner_dict = {'name':'','link':''}
    name = l.split(":")[0].strip()
    link = l.split(":")[1].strip()
    name_tags = name.split(" ")
    
    worksheet.write(i+1, 0, label = i)
    worksheet.write(i+1, 1, label = name)
    worksheet.write(i+1, 2, label = link)
    
    for j in range(0,len(name_tags)):
        worksheet.write(i+1, j+3, label = name_tags[j])
            
    inner_dict['name'] = name
    inner_dict['link'] = link
    playerDictionary[i] = inner_dict
    print("Read Line: "+str(i))

workbook.save('D:\\Python Scrapping Project\\files\\excel\\player\\playerProfile_'+file_name+'.xls')

with open('D:\\Python Scrapping Project\\files\\player\\data_'+file_name+'.json','w') as outfile:
    json.dump(playerDictionary,outfile)