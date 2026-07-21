name: Update Data and Build Site

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write
  id-token: write
  pages: write

jobs:
  update-and-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install requests urllib3

      - name: Run Build and Logo Downloader
        run: python build.py

      - name: Commit and Push new logos if downloaded
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@://github.com"
          
          # הכרחי: מוסיף את התיקייה הראשית למעקב הגיט
          git add assets/logos/
          
          if ! git diff-index --quiet HEAD; then
            git commit -m "chore: auto-download missing casino logos [skip ci]"
            git push origin main || git push origin master
            echo "✅ New logos saved into the repository permanently!"
          else
            echo "✨ No new logos were downloaded."
          fi

      - name: Upload production artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public/

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

