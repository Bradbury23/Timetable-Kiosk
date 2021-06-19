import sys, random, os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, Markup, redirect
from requests import get, session, post
from time import sleep, time

#Change this variable to change the port number that is used. 
portNumber = 5000
#Change this variable to either increase or decrease the auto-logout timer (recommended time is between 30 to 45 seconds). 
timeLimit = 30
#Change this to where you can access your kiosk server (used in redirect and in auto-logout).
serverAddress = "http://localhost:5000/login"
#Change this to your sentral address.
schoolName = '<school-name>' # E.G: lithgow-h
sentralAddress = f"https://{schoolName}.sentral.com.au/portal/"
sentralLoginAddress = f'https://{schoolName}.sentral.com.au/portal2/user/'
dashboardAddress = sentralAddress + 'dashboard'
#Delimeters (characters that will be cleared from both usernames and passwords).
delim = ['(', ')', '>', '<', ':', '{', '}', ';', '$']
logins, prints = [int(i) for i in open('stats', 'r').read().splitlines()]
app = Flask(__name__)
query = 0
#Change this variable to control the time a user is locked out for after printing.
tempBan = 15*60 #15 minutes.
#add users here to permanently ban them. 
#Syntax is: {'username': username, 'ban': False, 'time': time()}
blacklist = []
#Leave this variable blank.
username = ''

#If hit, redirects client to /login.
@app.route('/')
def reroute():
    return redirect(serverAddress)

@app.route('/login', methods=["GET", "POST"])
def home():
    query = random.randint(0, 100000)
    return render_template('index.html', random=query, version=open('version', 'r').read())

@app.route('/data', methods=["GET", "POST"])
def timetable():
    global logins, username
    with open('stats', 'w') as file:
        file.write(f'{logins}\n{prints}')
    logins += 1
    query = random.randint(0, 100000)
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        # input validation. 
        for d in delim:
            username = username.replace(d, '')
            password = password.replace(d, '')
        payload = {'action': 'login', 'username': username, 'password': password, 'remember_username': 'false'}
        del password
        try:
            if time()-blacklist[[i['username'] for i in blacklist].index(username)]['time'] >= tempBan:
                del blacklist[[i['username'] for i in blacklist].index(username)]
        except:
            pass
        if not (username in [i['username'] for i in blacklist]):
            s = session()
            loginResponse = s.post(sentralLoginAddress, data=payload)
            del payload
            dashboard = s.get(dashboardAddress)
            html = dashboard.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', {'class': 'timetable table'}) 
            try:
                notices = soup.find('div', {'class': 'span9'}).div
                user = soup.find('p', {'class': 'student-login'}).text.title()
                resetTime = timeLimit 
            except:
                notices = "ERROR"
                user = "ERROR"
                resetTime = 0
            table = table if table != None else "Invalid Credentials Please Try Again"
            render = render_template('data.html', version=open('version', 'r').read(), resetTime=resetTime, username=user, serverAddress=serverAddress, table=Markup(table), random=query, notices=Markup(str(notices).replace('<p><br/></p>', ''))).replace('/portal/student/getstaffphoto/', sentralAddress + 'student/getstaffphoto/')
            renderSoup = BeautifulSoup(render, 'html.parser')
            userpics = renderSoup.find_all('img', {'alt': 'Userpic'})
            imageUrls = [i['src'] for i in userpics]
            cache = 'static/images/UserPics'
            for imageUrl in imageUrls:
                arg = imageUrl.split('/')[-1]
                if not arg in os.listdir(cache.replace('/', os.path.sep)):
                    img = s.get(imageUrl)
                    open(f"{cache}/{imageUrl.split('/')[-1]}", 'wb').write(img.content)
                render = render.replace(sentralAddress + 'student/getstaffphoto/', f"{cache}/")
            s.get(sentralAddress + 'logout')
            return render
        else:
            return redirect(serverAddress)

@app.route('/print', methods=['GET'])
def statLog():
    global username, blacklist
    blacklist.append({'username': username, 'ban': False, 'time': time()})
    print('PRINTING')
    global logins, prints
    prints += 1
    with open('stats', 'w') as file:
        file.write(f'{logins}\n{prints}')
    return redirect(serverAddress)

@app.route('/stats', methods=['GET'])
def stats():
    return render_template('stats.html', totalLogins=open('stats', 'r').read().splitlines()[0], totalPrints=open('stats', 'r').read().splitlines()[1])

if __name__ == '__main__':
    app.run(host="localhost", port=portNumber)
