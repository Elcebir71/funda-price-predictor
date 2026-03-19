#!/bin/bash
# GitHub'a yükleme komutları - Copy-paste yapabilirsin

# 1. Proje klasörüne git
cd funda-price-predictor

# 2. Git başlat
git init

# 3. Tüm dosyaları ekle
git add .

# 4. İlk commit
git commit -m "Initial commit: Complete Funda Price Predictor ML project

- Web scraper for Funda.nl
- Feature engineering pipeline
- 6 ML models (Linear, RF, GB, XGBoost, etc.)
- Streamlit interactive dashboard
- Complete documentation and roadmap"

# 5. GitHub remote ekle (GitHub'da repo oluşturduktan SONRA çalıştır)
git remote add origin https://github.com/Elcebir71/funda-price-predictor.git

# 6. Main branch'e geç
git branch -M main

# 7. GitHub'a push
git push -u origin main

# İlk kez push yaparken GitHub credentials isteyecek:
# Username: Elcebir71
# Password: [Personal Access Token - GitHub settings'den oluştur]
