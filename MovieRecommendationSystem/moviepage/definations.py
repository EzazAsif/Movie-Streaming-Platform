from bs4 import BeautifulSoup
import requests

def get_first_image_url(query):
    # Perform a Google search
    search_url = f"https://www.google.com/search?hl=en&q={query}&tbm=isch"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        if images:
            # The first image might be the logo, so we go for the first relevant image in the search results
            first_image = images[1] if len(images) > 1 else images[0]
            return first_image['src']
    return None


def createlist(arra):
    array=[]
    for item in arra:
        array.append({'title':item,'picture':get_first_image_url(item+" movie poster 1920*1080")})
    return array
