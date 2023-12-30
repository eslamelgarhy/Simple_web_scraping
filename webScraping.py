import requests
from bs4 import BeautifulSoup
import csv
date = input("please enter date in the following format yyyy-mm-dd")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src , "lxml")
    matches_details = []

    champianships = soup.find_all("div" , {'class': 'matchCard'})
    
    def get_match_info(champianships):
        champianship_title = champianships.contents[1].find('h2').text.strip()
        all_matches = champianships.contents[3].find_all("div" , {'class':'item'})
        number_of_matches = len(all_matches)
        for i in range(number_of_matches):
            # get teams name
            team_a = all_matches[i].find("div",{'class':'teamA'}).text.strip()

            team_b = all_matches[i].find("div",{'class':'teamB'}).text.strip()

            # get score
            match_result = all_matches[i].find("div",{'class':'MResult'}).find_all('span',{'class':'score'})
            score = f"{match_result[0].text.strip()} -  {match_result[1].text.strip()}"

            # get match time 
            match_time = all_matches[i].find("div",{'class':'MResult'}).find("span",{'class':'time'}).text.strip()

            # add match info to matches_details
            matches_details.append({"نوع البطولة":champianship_title , "الفريق الاول":team_a ,"النتيجة":score, "الفريق الثاني":team_b ,
                                    "ميعاد المباراة ":match_time})

            

    for i in range(len(champianships)):
        get_match_info(champianships[i])

    keys = matches_details[0].keys()
    with open('Documents/scraping/matches-details.csv','w') as output_file :
        dict_writer =  csv.DictWriter(output_file,keys)    
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

main(page)    