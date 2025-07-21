import os 
import requests

from dotenv import load_dotenv

load_dotenv() 


# use mock = false to use the actual scrapper api, otherwise set to true to use a test json file 
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """ scrape information from Linkedin profiles, Manually scrape the informatio from the Linkedin profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPEN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get('person')

    #cleanse the data from empty fields, like certifications 
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["certifications"]
        }
    
    return data 


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/afham-bashir/"
        )
    )