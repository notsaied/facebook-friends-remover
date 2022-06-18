# BasmAllah
# Facebook Friends Remover
# Made By Ahmed Saied AKA Saiedoz
# username : notsaied
# Github:notsaied | Facebook@notsaied | Twitter:@saiedoz | Telegram@notsaied | instagram@notsaied
# https://notsaied.site

from re import S
import requests
from bs4 import BeautifulSoup
import json

class fb():
    
    cookie = '' # save cookie
        
    friends = [] # get all friends ids
        
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39'

    def __init__(self,email,password):
        
        self.email = email
        
        self.password = password
    
    # end init function

    def login(self):
        headers = {
            'authority': 'mbasic.facebook.com',
            'method': 'GET',
            'path': '/login/device-based/regular/login/?refsrc=deprecated&lwv=100',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }

        # get cookie and tokens for request to login

        rs = requests.get('https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100',headers=headers)

        soup = BeautifulSoup(rs.content,'html.parser')

        # get all tokens

        lsd = soup.select('input[name="lsd"]')[0]['value']
        
        jazoest = soup.select('input[name="jazoest"]')[0]['value']
        
        m_ts = soup.select('input[name="m_ts"]')[0]['value']
        
        li = soup.select('input[name="li"]')[0]['value']

        cookies = dict(rs.cookies.get_dict()) # get cookie to send request to login

        data = {
            'lsd':lsd,
            'jazoest':jazoest,
            'm_ts':m_ts,
            'li':li,
            'try_number':'0',
            'unrecognized_tries':'0',
            'email': self.email,
            'pass': self.password,
            'login': 'Log In',
            'bi_xrwh': '0'
        }
        headers['method'] = 'POST'
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        headers['content-type'] = 'application/x-www-form-urlencoded'
        headers['sec-fetch-site'] = 'same-origin'

        respone = requests.post('https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100',
        data=data,
        cookies=cookies,
        headers=headers,
        allow_redirects=False
        )
        self.cookie = respone.cookies.get_dict()
        return self.getCookie()

    # end login function

    def getCookie(self):
        if self.cookie == {}:
            print('[!] Login failed')
            exit()
        else:
            return '[!] Login Success'
    # end getCookie function

    def extract_friends(self,r):
        headers = {
            'authority': 'mbasic.facebook.com',
            'method':'GET',
            'path':'/friends',
            'scheme': 'https',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language':'en-US,en;q=0.9',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':self.user_agent
        }

        req = requests.get('https://mbasic.facebook.com/friends/center/friends/?ppk='+str(r),cookies=dict(self.cookie),headers=headers)
        soup = BeautifulSoup(req.content,'html.parser')
        friends = soup.select('.x > a')
        if len(friends) == 0:
            print('[!] Friends List Are Ready')
        else:    
            for friend in friends:
                self.friends.append(friend.get('href').split('&')[0].split('=')[1]) 
            self.extract_friends(r+1)
        return self.friends
    # end get friends function

    def remove(self,id):
        
        r = requests.get('https://mbasic.facebook.com/removefriend.php?friend_id='+id+'&unref=profile_gear',cookies=self.cookie)
        # get tokens
        soup = BeautifulSoup(r.content,'html.parser')

        jazoest = soup.select('input[name="jazoest"]')[0]['value']
        fb_dtsg = soup.select('input[name="fb_dtsg"]')[0]['value']

        headers = {
            'authority': 'mbasic.facebook.com',
            'method': 'POST',
            'path': '/a/friends/remove/?subject_id='+ id +'&unfriend_ref=profile_gear',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://mbasic.facebook.com',
            'referer': 'https://mbasic.facebook.com/removefriend.php?friend_id='+id+'&unref=profile_gear',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
       
        data = {
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'confirm': 'confirm'
        }
        rq = requests.post('https://mbasic.facebook.com/a/friends/remove/?subject_id='+id+'&unfriend_ref=profile_gear',
        data=data,
        cookies=self.cookie,
        headers=headers)

        return id+' Removed [!]'

    # end remove function

print('Hello, this is a Facebook Unfriender \nMade by : Saiedoz \nHope u can enjoy :)')

email = input('Enter your email : ')

password = input('Enter your password : ')

account = fb(email,password)

account.login()

friends = account.extract_friends(0)

print('\n[!] Total Friends : '+str(len(friends)))

print('\n[!] Start removing friends')

for friend in friends:
    
    print(account.remove(friend))

print('\n[!] Done')

# hope i can make u happy :)