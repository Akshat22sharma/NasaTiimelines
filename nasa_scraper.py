import requests
from bs4 import BeautifulSoup
import csv

class NasaTimeSeriesScraper:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def scrape(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = self.extract_data(soup)
            self.save_to_csv(data)
        else:
            print("Failed to retrieve the webpage.")
    
    def extract_data(self, soup):
        data = []
        items = soup.find_all('div', class_='item')
        for item in items:
            title = item.find('h2').text.strip()
            description = item.find('p').text.strip()
            data.append({'title': title, 'description': description})
        
        return data
    
    def save_to_csv(self, data):
        with open('nasa_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        print("Data saved to nasa_data.csv")

if __name__ == "__main__":
    nasa_url = "https://www.nnvl.noaa.gov/view/globaldata.html"
    nasa_scraper = NasaTimeSeriesScraper(nasa_url)
    nasa_scraper.scrape()
