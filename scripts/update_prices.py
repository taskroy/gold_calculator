"""Fetch today's UAE gold prices per gram from uaegoldprices.com and save them to prices.json."""
import json, re, sys, urllib.request
from html import unescape

URL = "https://uaegoldprices.com/"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (gold-calculator price update)"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

# Turn the page into plain text so table markup doesn't matter
text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
text = unescape(re.sub(r"<[^>]+>", " ", text))
text = text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩٫", "0123456789."))
text = re.sub(r"\s+", " ", text)

prices = {}
for k in ("24", "22", "21", "18"):
    # First AED price after the "عيار <k>" label, e.g. "سعر جرام الذهب عيار 24 491.53 133.93"
    m = re.search(r"عيار\s*" + k + r"\D{0,40}?(\d{2,4}(?:,\d{3})*\.\d{1,2})", text)
    if not m:
        sys.exit(f"Could not find the {k}K price. The website layout may have changed.")
    prices[k] = float(m.group(1).replace(",", ""))

if not (prices["18"] < prices["21"] < prices["22"] < prices["24"]):
    sys.exit(f"Prices look wrong, not saving: {prices}")

date = re.search(r"(20\d\d)/(\d{1,2})/(\d{1,2})", text)
time = re.search(r"الساعة\s*(\d{1,2}:\d{2})", text)
out = {
    "date": f"{date.group(1)}-{int(date.group(2)):02d}-{int(date.group(3)):02d}" if date else "",
    "time": time.group(1) if time else "",
    **prices,
}
with open("prices.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("Saved:", out)
