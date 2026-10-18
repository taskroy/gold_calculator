# Gold Making Charge Calculator

Works out how much a UAE gold shop is charging on top of the gold (the factory cut per gram).
Prices come from uaegoldprices.com and update automatically three times a day.

- `index.html` is the calculator page.
- `prices.json` holds today's prices. A GitHub Action updates it.
- `scripts/update_prices.py` reads the prices from uaegoldprices.com.
- `.github/workflows/update-prices.yml` runs the update at 8:45, 12:45 and 17:45 Dubai time.
  To update now, open the Actions tab, choose "Update gold prices", then "Run workflow".
