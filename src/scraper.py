"""
Funda.nl Web Scraper
Collects house listings from Funda.nl

Usage:
    python scraper.py --city amsterdam --max-pages 10
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import argparse
from datetime import datetime
import json
import os
from tqdm import tqdm


class FundaScraper:
    def __init__(self, city="amsterdam", property_type="koop"):
        """
        Initialize Funda scraper
        
        Args:
            city: City name (amsterdam, utrecht, rotterdam, etc.)
            property_type: "koop" (buy) or "huur" (rent)
        """
        self.city = city
        self.property_type = property_type
        self.base_url = f"https://www.funda.nl/zoeken/{property_type}/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.listings = []
    
    def get_search_results_page(self, page_num=1):
        """
        Get listings from a search results page
        
        Args:
            page_num: Page number to scrape
            
        Returns:
            List of listing URLs
        """
        search_url = f"{self.base_url}?selected_area=%5B%22{self.city}%22%5D"
        if page_num > 1:
            search_url += f"&search_result={page_num}"
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all listing cards
            listings = soup.find_all('div', {'data-test-id': 'search-result-item'})
            
            urls = []
            for listing in listings:
                link = listing.find('a', href=True)
                if link:
                    url = link['href']
                    if url.startswith('/'):
                        url = f"https://www.funda.nl{url}"
                    urls.append(url)
            
            return urls
        
        except Exception as e:
            print(f"Error fetching page {page_num}: {e}")
            return []
    
    def parse_listing(self, url):
        """
        Parse individual listing page
        
        Args:
            url: Listing URL
            
        Returns:
            Dictionary with listing details
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize data dictionary
            data = {
                'url': url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Price
            price_elem = soup.find('strong', {'data-test-id': 'price-sale'})
            if price_elem:
                price_text = price_elem.text.strip().replace('€', '').replace('.', '').replace(',', '').strip()
                try:
                    data['price'] = int(''.join(filter(str.isdigit, price_text)))
                except:
                    data['price'] = None
            
            # Address
            address_elem = soup.find('h1', class_='object-header__title')
            if address_elem:
                data['address'] = address_elem.text.strip()
            
            # Postcode and city
            location_elem = soup.find('h2', class_='object-header__subtitle')
            if location_elem:
                location_text = location_elem.text.strip()
                data['location'] = location_text
                # Extract postcode (format: 1234 AB)
                import re
                postcode_match = re.search(r'\d{4}\s*[A-Z]{2}', location_text)
                if postcode_match:
                    data['postcode'] = postcode_match.group().replace(' ', '')
            
            # Features (m², kamers, etc.)
            features = soup.find_all('dl', class_='object-kenmerken-list')
            for feature_list in features:
                dts = feature_list.find_all('dt')
                dds = feature_list.find_all('dd')
                
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip().lower()
                    value = dd.text.strip()
                    
                    if 'woonoppervlakte' in key:
                        data['living_area_m2'] = self._extract_number(value)
                    elif 'perceel' in key and 'oppervlakte' in key:
                        data['plot_area_m2'] = self._extract_number(value)
                    elif 'aantal kamers' in key:
                        data['rooms'] = self._extract_number(value)
                    elif 'aantal slaapkamers' in key:
                        data['bedrooms'] = self._extract_number(value)
                    elif 'bouwjaar' in key:
                        data['build_year'] = self._extract_number(value)
                    elif 'energielabel' in key:
                        data['energy_label'] = value
                    elif 'soort woning' in key:
                        data['house_type'] = value
                    elif 'soort bouw' in key:
                        data['construction_type'] = value
            
            # Description
            description_elem = soup.find('div', {'data-test-id': 'object-description-body'})
            if description_elem:
                data['description'] = description_elem.text.strip()[:500]  # First 500 chars
            
            return data
        
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return None
    
    def _extract_number(self, text):
        """Extract first number from text"""
        import re
        match = re.search(r'\d+', text.replace('.', '').replace(',', ''))
        if match:
            return int(match.group())
        return None
    
    def scrape(self, max_pages=10, delay=2):
        """
        Scrape multiple pages
        
        Args:
            max_pages: Maximum number of search result pages to scrape
            delay: Delay between requests (seconds)
        """
        print(f"Starting scrape for {self.city} (max {max_pages} pages)")
        
        all_urls = []
        for page in range(1, max_pages + 1):
            print(f"Fetching page {page}...")
            urls = self.get_search_results_page(page)
            all_urls.extend(urls)
            time.sleep(delay)
            
            if not urls:  # No more results
                break
        
        print(f"\nFound {len(all_urls)} listings. Parsing details...")
        
        for url in tqdm(all_urls):
            listing_data = self.parse_listing(url)
            if listing_data:
                self.listings.append(listing_data)
            time.sleep(delay)  # Be respectful
        
        print(f"\nSuccessfully scraped {len(self.listings)} listings")
    
    def save_to_csv(self, filename=None):
        """Save listings to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/funda_{self.city}_{timestamp}.csv"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(self.listings)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        return filename


def main():
    parser = argparse.ArgumentParser(description='Scrape Funda.nl listings')
    parser.add_argument('--city', type=str, default='amsterdam', help='City to scrape')
    parser.add_argument('--max-pages', type=int, default=10, help='Max pages to scrape')
    parser.add_argument('--delay', type=float, default=2, help='Delay between requests')
    
    args = parser.parse_args()
    
    scraper = FundaScraper(city=args.city)
    scraper.scrape(max_pages=args.max_pages, delay=args.delay)
    scraper.save_to_csv()


if __name__ == "__main__":
    main()
