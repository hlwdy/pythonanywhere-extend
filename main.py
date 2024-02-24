import requests,json
import re,os

if('USNAME' not in os.environ):
    print('no secret')
    exit()

usname=os.environ["USNAME"]
password=os.environ["PASSWORD"]
url=os.environ["URL"]

headers = {
    'Referer': 'https://www.pythonanywhere.com/login/',
    'Origin': 'https://www.pythonanywhere.com',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.421.0 Safari/537.36",
    'Accept': "*/*",
    'Connection': 'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
}

s=requests.session()
r=s.get('https://www.pythonanywhere.com/login',headers=headers)
csrf_token=re.findall('Anywhere.csrfToken = "(.*?)";',r.text)[0]
print(csrf_token)

data = {
    'csrfmiddlewaretoken':csrf_token,
    'auth-username': usname,
    'auth-password': password,
    'login_view-current_step': 'auth',
}
r=s.post('https://www.pythonanywhere.com/login/',headers=headers,data=data)
#print(r.text)

r=s.get('https://www.pythonanywhere.com/user/'+usname+'/webapps/#tab_id_'+url.replace('.','_'),headers=headers)
csrf_token=re.findall('Anywhere.csrfToken = "(.*?)";',r.text)[0]
print(csrf_token)

data = {
    'csrfmiddlewaretoken':csrf_token,
}
headers['Referer']='https://www.pythonanywhere.com/user/'+usname+'/webapps/'
r=s.post('https://www.pythonanywhere.com/user/'+usname+'/webapps/'+url+'/extend',headers=headers,data=data)
print(r.status_code)
