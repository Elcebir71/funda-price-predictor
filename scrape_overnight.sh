#!/bin/bash

echo "🌙 Starting overnight scraping at $(date)"
echo "================================================"
cd ~/Downloads/funda-price-predictor/
pwd
cities=("amsterdam" "utrecht" "rotterdam" "den-haag" "eindhoven")
source venv/bin/activate
for city in "${cities[@]}"; do
  echo ""
  echo "🏙️  Starting $city at $(date)"
  python src/funda_scraper_selenium.py --city "$city" --max-pages 25
  
  if [ $? -eq 0 ]; then
    echo "✅ $city completed at $(date)"
  else
    echo "❌ $city failed at $(date)"
  fi
done

echo ""
echo "================================================"
echo "🎉 All cities completed at $(date)"
echo ""
echo "📊 Results:"

# Eğer dosyalar varsa göster, yoksa "henüz yok" de
if ls data/raw/funda_*.csv 1> /dev/null 2>&1; then
  ls -lh data/raw/funda_*.csv
else
  echo "No CSV files found yet"
fi
