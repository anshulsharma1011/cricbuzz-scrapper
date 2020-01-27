import sys

import xlrd 
import xlwt
sys.path.append('D:\\Python Scrapping Project')

path = 'D:\\Python Scrapping Project\\files\\excel\\player\\'

file_name_array = ['playerProfile_player_profile.xls','playerProfile_player_profile_updated_1.xls','playerProfile_player_profile_updated_4000_5000.xls','playerProfile_player_profile_updated_5000_6000.xls','playerProfile_player_profile_updated_6000_7000.xls','playerProfile_player_profile_updated_7000.xls','playerProfile_player_profile_updated_10000_1.xls','playerProfile_player_profile_updated_12000_3.xls'] 


workbook = xlwt.Workbook(encoding = 'ascii')
writeSheet = workbook.add_sheet('playerProfileLink')
ind = 0
for i in range(len(file_name_array)):
    print("Reading File: " + file_name_array[i])
    loc = path+file_name_array[i]
    wb = xlrd.open_workbook(loc)
    readSheet = wb.sheet_by_index(0)
    cols = readSheet.ncols
    rows = readSheet.nrows
    for j in range(rows):
        for k in range(cols):
            writeSheet.write(ind, k, label = readSheet.cell_value(j,k))
            print("Cell Number: " + str(j) + "," + str(k))
        ind = ind + 1
            
            
workbook.save('D:\\Python Scrapping Project\\files\\excel\\playersFinal.xls')