from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import argparse
from datetime import datetime
import os
from tqdm import tqdm
import random
import re


class FundaScraper:
    def __init__(self, city="amsterdam", property_type="koop"):
        self.city = city.lower()
        self.property_type = property_type
        self.base_url = "https://www.funda.nl"
        self.listings = []
        self.driver = None
        
    def init_driver(self):
        """Initialize Selenium WebDriver"""
        options = Options()
        options.add_argument('--headless')  # Run without GUI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Chrome WebDriver initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Chrome: {e}")
            print("💡 Install ChromeDriver:")
            print("   Mac: brew install chromedriver")
            print("   Linux: apt install chromium-chromedriver")
            print("   Or download: https://chromedriver.chromium.org/")
            raise
    
    def get_search_results_page(self, page_num=1):
        """Scrape search results page with Selenium"""
        # Dutch URL format (more listings available)
        search_url = f"https://www.funda.nl/zoeken/{self.property_type}/?selected_area=%5B%22{self.city}%22%5D"
        if page_num > 1:
            search_url += f"&search_result={page_num}"
        
        try:
            print(f"🔍 Loading: {search_url[:60]}...")
            self.driver.get(search_url)
            
            # Wait for JavaScript to load listings
            time.sleep(random.uniform(3, 5))
            
            # Get page source after JS execution
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find all listing links
            # Funda listing URLs: /koop/amsterdam/huis-123456/
            urls = []
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link['href']
                # Match patterns like: /koop/city/huis-* or /koop/city/appartement-*
                if f'/{self.property_type}/' in href and any(p in href for p in ['/huis-', '/appartement-', '/woonhuis-']):
                    if 'filters' not in href and 'kaart' not in href:
                        full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                        clean_url = full_url.split('?')[0].split('#')[0]
                        urls.append(clean_url)
            
            unique_urls = list(set(urls))
            print(f"✅ Found {len(unique_urls)} listings on page {page_num}")
            
            return unique_urls
            
        except Exception as e:
            print(f"❌ Error on page {page_num}: {e}")
            return []
    
    def parse_listing(self, url):
        """Parse individual listing page"""
        try:
            time.sleep(random.uniform(2, 4))  # Be respectful
            
            self.driver.get(url)
            time.sleep(3)  # Wait for JS
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            data = {
                'url': url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract all text content for pattern matching
            page_text = soup.get_text()
            
            # Price - multiple patterns
            price_patterns = [
                r'€\s*([\d.]+)',  # € 350.000
                r'(\d+\.\d+)\s*k\.k\.',  # 350.000 k.k.
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, page_text)
                if match:
                    price_str = match.group(1).replace('.', '')
                    try:
                        data['price'] = int(price_str)
                        break
                    except:
                        pass
            
            # Living area (m²)
            if 'm²' in page_text or 'm2' in page_text:
                area_match = re.search(r'(\d+)\s*m[²2]', page_text)
                if area_match:
                    data['living_area_m2'] = int(area_match.group(1))
            
            # Rooms / Kamers
            rooms_patterns = [
                r'(\d+)\s*kamer',
                r'(\d+)\s*room',
            ]
            for pattern in rooms_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    data['rooms'] = int(match.group(1))
                    break
            
            # Bedrooms / Slaapkamers
            bedroom_patterns = [
                r'(\d+)\s*slaapkamer',
                r'(\d+)\s*bedroom',
            ]
            for pattern in bedroom_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    data['bedrooms'] = int(match.group(1))
                    break
            
            # Build year / Bouwjaar
            year_match = re.search(r'bouwjaar[:\s]+(\d{4})', page_text, re.IGNORECASE)
            if not year_match:
                year_match = re.search(r'built[:\s]+(\d{4})', page_text, re.IGNORECASE)
            if year_match:
                data['build_year'] = int(year_match.group(1))
            
            # Energy label
            energy_match = re.search(r'energielabel[:\s]+([A-G][\+]*)', page_text, re.IGNORECASE)
            if energy_match:
                data['energy_label'] = energy_match.group(1)
            
            # Address (from title)
            title_elem = soup.find('h1')
            if title_elem:
                data['address'] = title_elem.get_text(strip=True)[:100]
            
            return data if 'price' in data or 'living_area_m2' in data else None
            
        except Exception as e:
            print(f"⚠️  Error parsing {url}: {str(e)[:100]}")
            return None
    
    def scrape(self, max_pages=3, delay=3):
        """Main scraping loop"""
        print(f"🚀 Starting Funda scrape for {self.city}")
        print(f"📄 Max pages: {max_pages}")
        
        # Initialize driver
        self.init_driver()
        
        try:
            # Get listing URLs from search pages
            all_urls = []
            for page in range(1, max_pages + 1):
                urls = self.get_search_results_page(page)
                if not urls:
                    print(f"⚠️  No listings found on page {page}. Stopping.")
                    break
                all_urls.extend(urls)
                time.sleep(delay)
            
            print(f"\n📋 Found {len(all_urls)} total listings")
            print(f"🔄 Parsing details...")
            
            # Parse each listing
            for url in tqdm(all_urls):
                result = self.parse_listing(url)
                if result:
                    self.listings.append(result)
            
            print(f"\n🏁 Successfully scraped {len(self.listings)} listings")
            
        finally:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed")
    
    def save_to_csv(self):
        """Save results to CSV"""
        if not self.listings:
            print("❌ No data to save")
            return None
        
        os.makedirs('data/raw', exist_ok=True)
        df = pd.DataFrame(self.listings)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/raw/funda_{self.city}_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        print(f"💾 Saved {len(df)} listings to {filename}")
        
        # Show preview
        print(f"\n📊 Data preview:")
        print(df.head())
        print(f"\n📈 Stats:")
        if 'price' in df.columns:
            print(f"  Avg price: €{df['price'].mean():,.0f}")
        if 'living_area_m2' in df.columns:
            print(f"  Avg area: {df['living_area_m2'].mean():.0f} m²")
        
        return filename


def main():
    parser = argparse.ArgumentParser(description='Scrape Funda.nl listings')
    parser.add_argument('--city', default='amsterdam', help='City name')
    parser.add_argument('--max-pages', type=int, default=2, help='Max search pages')
    parser.add_argument('--delay', type=int, default=3, help='Delay between pages')
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════╗
║   FUNDA.NL SCRAPER (Selenium)        ║
║   City: {args.city:<26} ║
║   Pages: {args.max_pages:<25} ║
╚══════════════════════════════════════╝
    """)
    
    scraper = FundaScraper(city=args.city)
    scraper.scrape(max_pages=args.max_pages, delay=args.delay)
    scraper.save_to_csv()


if __name__ == "__main__":
    main()
