from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
#count = 1

def find_winner(match_no,bsObj,worksheet,ind):
    result = ""
    winner = ""
    special_case = ""
    res = ""
    
    try:
        result = bsObj.find_all("div",{"class":"cb-text-complete"})[0].get_text()
    except IndexError:
        #print("No Data Found for match" + str(match_no))
        pass
    
    if result != "":
        #print(result)
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
                #print(winner +" ( "+special_case+" )")
            else:
                index = result.index('won')
                winner = (' '.join(result[:index]))
                if '(D/L' in result:
                    special_case = 'D/L method'
                    #print(winner +" ( "+special_case+" )")
                else:
                   # print(winner)
                    special_case = ""
        
        elif 'abandoned' in result or 'tied' in result or 'result' in result or 'drawn' in result:    
            winner = ("NA")
            res = "NA"
           # print(winner)
    
        else:
            winner = "WTF"
            res = "WTF"
           # print("WHAT THE FUCK")
            
            
    worksheet.write(ind, 0, label = match_no)
    worksheet.write(ind, 1, label = ' '.join(result))
    worksheet.write(ind, 2, label = res)
    worksheet.write(ind, 3, label = winner)
    worksheet.write(ind, 4, label = special_case)
    
    dic = {
            'match_no':match_no,
            'result_dec':' '.join(result),
            'result':res,
            'winner':winner,
            'special_case':special_case
            }
    
    return dic