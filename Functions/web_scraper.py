import re
import requests
from bs4 import BeautifulSoup


def main():
    show_name = input("Enter the name of the show: ")
    text_id = get_id(show_name)
    if text_id is None:
        print("Show not found")
        return
    score = get_score(text_id)
    print(f"The score of {show_name} is {score}")

def get_id(show_name):
    """
    Get the id of the mal show with the given name
    
    Input: show_name (str)
    Output: id (str)
    """
    search_url = f"https://myanimelist.net/anime.php?cat=anime&q={show_name}"               
    response = requests.get(search_url)                                                     
    soup = BeautifulSoup(response.content, "html.parser")                                   
    search_result = soup.find("td", width="45")                                             
    while search_result is not None:                                                        
        if search_result.text.strip() == "TV":
            search_result = search_result.find_previous("div", class_="title").a
            url = search_result["href"]
            id = re.findall(r"\d+", url)[0]
            return id
        search_result = search_result.find_next("td", width="45")
    return None


def get_score(text_id):
    """
    Get the score of the mal show with the given id
    
    Input: text_id (str)
    Output: score (str)
    """
    response = requests.get("https://myanimelist.net/anime/"+text_id)
    soup = BeautifulSoup(response.content, "html.parser")
    score_class = re.compile("score-label score-\d+")
    score = soup.find("div", class_=score_class).text
    return score
#NICE

if __name__ == "__main__":
    main()
