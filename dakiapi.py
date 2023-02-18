import requests

url = 'https://pterodactyl.file.properties/api/client/servers/f29d65b1/power'
headers = {
    "Authorization": "${{ secrets.DAKI_API_TOKEN }}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
}
payload = '{ "signal": "restart" }'

response = requests.request('POST', url, data=payload, headers=headers)
print(response.text)
