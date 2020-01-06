from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random
import xlrd
import xlwt


count = 1

workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('Winners Data')
worksheet.write(0, 0, label = 'Match Index')
worksheet.write(0, 1, label = 'Result Description')
worksheet.write(0, 2, label = 'Result')
worksheet.write(0, 3, label = 'Winner')
worksheet.write(0, 4, label = 'Special Case')

while count<=100:
    match_no = random.randint(3000,4000) 
    print(match_no) 
    req = Request("https://www.cricbuzz.com/api/html/cricket-scorecard/"+str(match_no), headers = {'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    bsObj = BeautifulSoup(webpage, 'lxml')
    result = ""
    winner = ""
    special_case = ""
    res = ""
    try:
        result = bsObj.find_all("div",{"class":"cb-text-complete"})[0].get_text()
    except IndexError:
        print("No Data Found for match" + str(match_no))
        
        
    if result != "":
        print(result)
        result = result.split()
        
        if 'won' in result:
            res = "WON"
            if 'tied' in result:
                index_won = result.index('won')
                index_tied = result.index('tied')
                st = result[index_tied+1:index_won]
                st = ' '.join(st).strip()
                winner = (''.join(st.split('(')))
                if 'bowl-out)' in result:
                    special_case = 'Bowl-Out'
                else:
                    special_case = 'Super-Over'
                print(winner +" ( "+special_case+" )")
            else:
                index = result.index('won')
                winner = (' '.join(result[:index]))
                if '(D/L' in result:
                    special_case = 'D/L method'
                    print(winner +" ( "+special_case+" )")
                else:
                    print(winner)
                    special_case = ""
        
        elif 'abandoned' in result or 'tied' in result or 'result' in result or 'drawn' in result:    
            winner = ("NA")
            res = "NA"
            print(winner)
    
        else:
            winner = "WTF"
            res = "WTF"
            print("WHAT THE FUCK")
    
    worksheet.write(count, 0, label = match_no)
    worksheet.write(count, 1, label = ' '.join(result))
    worksheet.write(count, 2, label = res)
    worksheet.write(count, 3, label = winner)
    worksheet.write(count, 4, label = special_case)
    
    count = count+1

workbook.save('C:\\Users\\Anshul Sharma\\Desktop\\winnersTest.xls')