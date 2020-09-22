import requests

url = 'https://www.google.com/amp/s/www.nytimes.com/2020/09/19/science/venus-planets-microbes-life.amp.html'
redirect_to = 'https://www.nytimes.com/2020/09/19/science/venus-planets-microbes-life.html'

r = requests.get(url) # From what I've found, request.history[0] is the request that redirected, if it was a redirect

#print(r.is_redirect)


r = requests.get(url)

print(r.text)