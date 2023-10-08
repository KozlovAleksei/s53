import time
print('start')

gNetRoot = ''

def main(test):
    if test:
        # test
        base_url = 'https://testnet.binance.vision'  # https://youtu.be/NczNjVxwx3A?t=636
        api_key = 'LDt6vLKawn1VYaAs8CTwYx6RtAiVrowVe3wu1bRerko9VZ0HAr2gL7KMMS3kM5DH'
        api_secret = 'nvXZgMuLaQNlbGO8STgdzMYixrhuPEwPL641F3AXwelU9LgqRDz4iYYyoWSxZDRE'
        gNetRoot = "Z:\\#TEST\\"
    else:
        # real
        base_url = 'https://api2.binance.com'  # https://binance-docs.github.io/apidocs/spot/en/#general-info
        api_key = '1'
        api_secret = '2'
        gNetRoot = "Z:\\#REAL\\"



    print('gNetRoot=', gNetRoot)
    while True:
        print('gNetRoot2=', gNetRoot)
        time.sleep(12)
