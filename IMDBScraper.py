from bs4 import BeautifulSoup
import requests, openpyxl

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

excell = openpyxl.Workbook()
sheet= excell.active
sheet.title = "IMDB's top rated movies"
sheet.append(["Rank","Name", "Year Of Release","IMDB rating"])

try:
    websiteLink = requests.get("https://www.imdb.com/chart/top/", headers=headers)
    websiteLink.raise_for_status()

    soup = BeautifulSoup(websiteLink.text, "html.parser")
    
    movies = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-3f13560f-0 sTTRj compact-list-view ipc-metadata-list--base").find_all("li", class_ = "ipc-metadata-list-summary-item sc-59b6048d-0 jemTre cli-parent")
    

    for movie in movies:
        name = movie.find("div", class_="ipc-metadata-list-summary-item__c").find("div",class_= "ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-4dcdad14-9 dZscOy cli-title").find("a", class_="ipc-title-link-wrapper").find("h3", class_= "ipc-title__text").get_text(strip=True).split(". ")[1]
        rank = movie.find("div", class_="ipc-metadata-list-summary-item__c").find("div",class_= "ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-4dcdad14-9 dZscOy cli-title").find("a", class_="ipc-title-link-wrapper").find("h3", class_= "ipc-title__text").get_text(strip=True).split(".")[0]
        year = movie.find("div", class_="ipc-metadata-list-summary-item__c").find("div",class_= "sc-4dcdad14-7 enzKXX cli-title-metadata").find("span", class_="sc-4dcdad14-8 cvucyi cli-title-metadata-item").text
        rating = movie.find("div", class_="ipc-metadata-list-summary-item__c").find("div",class_= "ipc-metadata-list-summary-item__tc").find("div", class_="sc-4dcdad14-0 hqxhHZ cli-children").find("span", class_="sc-4dcdad14-1 dAJxst").find("div",class_="sc-e3e7b191-0 iKUUVe sc-4dcdad14-2 bYaHFC cli-ratings-container").find("span",class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").get_text(strip=True).split("(")[0]
        print(f"{rank}. {name} {year} {rating} \n")
        sheet.append([rank,name,year,rating])
        
        

except Exception as e:
    print(e)

excell.save("IMDB's top 250 movies")


