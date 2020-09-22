import utils

url = 'https://www.google.com/amp/s/www.nytimes.com/2020/09/19/science/venus-planets-microbes-life.amp.html'
swiss_url = 'https://www.google.ch/amp/s/www.nytimes.com/2020/09/19/science/venus-planets-microbes-life.amp.html'
redirect_to = 'https://www.nytimes.com/2020/09/19/science/venus-planets-microbes-life.html'

print(utils.amp_to_normal(url))
print(utils.amp_to_normal(swiss_url))
print(utils.amp_to_normal(redirect_to))
