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



path = 'D:\\Python Scrapping Project\\files\\player\\'
file_names = ['player_profile.txt','player_profile_updated_1.txt','player_profile_updated_4000_5000.txt','player_profile_updated_5000_6000.txt','player_profile_updated_6000_7000.txt','player_profile_updated_7000.txt','player_profile_updated_10000_1.txt','player_profile_updated_12000_3.txt']

playerDictionary = {}

ind = 1
for x in range(0,len(file_names)):
    f = open(path+file_names[x],"r")
    arr = list(set(f))
    
    for i,l in enumerate(arr):
        name = l.split(":")[0].strip()
        link = l.split(":")[1].strip()
        playerDictionary[name] = link

print(playerDictionary)


for key,val in playerDictionary.items():
    name = key
    link = val
    name_tags = name.split(" ")
    
    worksheet.write(ind, 0, label = ind)
    worksheet.write(ind, 1, label = name)
    worksheet.write(ind, 2, label = link)
    
    for j in range(0,len(name_tags)):
        worksheet.write(ind, j+3, label = name_tags[j])
    
    ind = ind+1
    print(ind)

workbook.save('D:\\Python Scrapping Project\\files\\excel\\playerFinal.xls')

with open('D:\\Python Scrapping Project\\files\\player\\data_players.json','w') as outfile:
    json.dump(playerDictionary,outfile)