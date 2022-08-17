from django.shortcuts import render, HttpResponse, redirect
from home.models import Data
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import schedule 


# Create your views here.

import asyncio
from bs4 import BeautifulSoup
import time
import pprint
import json

# date = '2020-08-03'

async def get_html():
    import random
    from playwright.async_api import async_playwright
    user_agent_r = [
        'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/100.0.4896.127 '
        'Safari/537.17',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.0 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.0 '
        'Safari/537.36',
    ]
    user_agent_r = random.choice(user_agent_r)

    async with async_playwright() as p:
        page = await p.chromium.launch(headless=True)
        browser = await page.new_page(
            user_agent=user_agent_r
        )

        await browser.goto('https://api.nasdaq.com/api/calendar/dividends')

        # source = await browser.inner_html("*")
        
        html_content = await browser.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        data = soup.find('pre').text        
        
        j = {}
        j = json.loads(data)

        j=j["data"]["calendar"]["rows"]

        return j

def saveindb():
    j = asyncio.run(get_html())
    
    if j == None:
            d = Data(companyName="None", symbol="None", dividend_Ex_Date="None", payment_Date="None", record_Date="None", dividend_Rate=0, indicated_Annual_Dividend=0, announcement_Date="None")
            d.save()
    else:
        for i in j:
            companyName = i["companyName"]
            symbol = i["symbol"]
            dividend_Ex_Date = i["dividend_Ex_Date"]
            payment_Date = i["payment_Date"]
            record_Date = i["record_Date"]
            dividend_Rate = i["dividend_Rate"]
            indicated_Annual_Dividend = i["indicated_Annual_Dividend"]
            announcement_Date = i["announcement_Date"]

            d = Data(companyName=companyName, symbol=symbol, dividend_Ex_Date=dividend_Ex_Date, payment_Date=payment_Date, record_Date=record_Date, dividend_Rate=dividend_Rate, indicated_Annual_Dividend=indicated_Annual_Dividend, announcement_Date=announcement_Date)
            d.save()

schedule.every(24).hours.do(saveindb)


def home(request):
    if request.user.is_anonymous:
        return(redirect("/login"))
    else:
        schedule.run_pending()
        # time.sleep(14)
        data = None
        date_data = None
        if 'date' in request.GET:
            date = request.GET.get('date')

            if date != '':
                spl = date.split('-')
                year = spl[0]
                month = spl[1]
                day=spl[-1]
                date = month + '/' + day + '/' + year
                date_data = Data.objects.filter(dividend_Ex_Date=date).values()
            else: 
                date_data = Data.objects.filter().values()
            
            print(date)
            
        return render(request, 'core/home.html', {'Stock': date_data})


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check if user has enetered correct cridentials
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return(redirect("/"))
        else:
            # No backend authenticated the credentials
            return(render(request, 'login.html'))
    return(render(request, 'login.html'))

    
def logoutUser(request):
    logout(request)
    return(redirect('/login'))

