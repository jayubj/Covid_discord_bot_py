import discord
from discord.ext import commands
import requests
from datetime import datetime, timedelta
import aiohttp 
import os 

TOKEN = 'ODUzODUyODY5NzQwNTkzMTkz.YMbacw.JdWrCUE6rLlMi5LBmo3dSJSbaFQ'

client = commands.Bot(command_prefix='!')

os.environ["TH"] = "UTC+7"

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command()
async def thailand(ctx):
    r = requests.get(url = 'https://disease.sh/v3/covid-19/countries/Thailand') 
    response = r.json()
    print(response)
    datestr = datetime.fromtimestamp(response["updated"] / 1e3) 
    embedVar = discord.Embed(title=':flag_th:' +response["country"] +':syringe:', description=datestr.strftime("Last update %A %d/%m/%Y, %H:%M:%S") , color=0x00ff00)
    embedVar.add_field(name=":thermometer_face:ผู้ป่วยทั้งหมด", value='{:,}'.format(response["cases"]), inline=True)
    embedVar.add_field(name=":mask:ผู้ป่วยวันนี้", value='{:,}'.format(response["todayCases"]), inline=True)
    embedVar.add_field(name=":skull:เสียชีวิตทั้งหมด", value='{:,}'.format(response["deaths"]), inline=True)
    embedVar.add_field(name=":skull_crossbones:เสียชีวิตวันนี้", value='{:,}'.format(response["todayDeaths"]), inline=True)
    embedVar.add_field(name=":mechanical_arm:รักษาหายทั้งหมด", value='{:,}'.format(response["recovered"]), inline=True)
    embedVar.add_field(name=":muscle:รักษาหายวันนี้", value='{:,}'.format(response["todayRecovered"]), inline=True)
    embedVar.add_field(name=":hospital:รักษาตัวในโรงพยาบาล", value='{:,}'.format(response["active"]), inline=True)
    embedVar.set_footer(text="beta test bot code by Isabella#3446")

    await ctx.send(embed=embedVar)

@client.command()
async def covid(ctx, arg=None):
    if arg is None:
        return await ctx.send('พิมพ์ "!covid [ชื่อจังหวัด]" เพื่อตรวจสอบผู้ติดเชื้อในจังหวัด')
    else:
        r = requests.get(url = 'https://s.isanook.com/an/0/covid-19/static/data/thailand/accumulate/latest.json?1')
        response = r.json()
        r = requests.get(url = response['url']+'?1')
        response = r.json()
        all_provinces_data = response['data']

        province_data = next(filter(lambda province_obj : province_obj["slug"] == arg or province_obj['title'] == arg, all_provinces_data), None)
        if (province_data != None):
            currStats = province_data['currentStatus']
            datestr = datetime.strptime(response["lastUpdated"], '%Y-%m-%d') + timedelta(hours=8, minutes=29)
            embedVar = discord.Embed(title=':pill:'+province_data["slug"] +':syringe: ', description=datestr.strftime("ข้อมูลล่าสุด: %A %d/%m/%Y, %H:%M:%S"), color=0x00ff00)
            embedVar.add_field(name=":thermometer_face:ผู้ป่วยทั้งหมด", value='{:,}'.format(currStats["accumulate"]), inline=True)
            embedVar.add_field(name=":mask:ผู้ป่วยวันนี้", value='{:,}'.format(currStats["new"]), inline=True)
            embedVar.add_field(name=":chart_with_upwards_trend:อัตราการเกิดเชื้อในรูปแบบเปอร์เซนต์", value='{:,}'.format(currStats["infectionLevelByPercentile"]), inline=False)
            embedVar.add_field(name=":bar_chart: ระดับการติดเชื้อ", value='{:,}'.format(currStats["infectionLevelByRule"]), inline=True)
            embedVar.set_footer(text="beta test bot code by Isabella#3446")
            return await ctx.send(embed=embedVar)
        else:
            return await ctx.send('ไม่พบจังหวัดนี้')
            
@client.command()
async def vaccine(ctx, arg = None):
    if (arg is None):
        return await ctx.send('พิมพ์ !vaccine [ชื่อย่อประเทศ หรือ ชื่อประเทศ] เพื่อตรวจสอบวัคซีนในประเทศ')
    else:
        r = requests.get(url = 'https://disease.sh/v3/covid-19/countries/'+arg)
        response = r.json()
        if ("message" in response) : return await ctx.send(response['message'])
        updatetime = response["updated"]
        countryiso2 = response["countryInfo"]["iso2"]
        r = requests.get(url = 'https://disease.sh/v3/covid-19/vaccine/coverage/countries/'+arg+'?lastdays=1')
        response = r.json()
        print(response)
        datestr = datetime.fromtimestamp(updatetime / 1e3)
        embedVar = discord.Embed(title=f':flag_{countryiso2.lower()}: {response["country"]}', description=datestr.strftime("%A %d/%m/%Y, %H:%M:%S"), color=0x00ff00)
        embedVar.add_field(name="ยอดฉีดวัคซีน", value='{:,}'.format(list(response["timeline"].values())[0]), inline=True)
        embedVar.set_footer(text="beta test bot code by Isabella#3446")
        await ctx.send(embed=embedVar)


@client.command()
async def world(ctx, arg):
    if (arg is None):
        return await ctx.send('พิมพ์ "!world [ชื่อย่อประเทศ หรือ ชื่อประเทศ]" เพื่อตรวจสอบผู้ติดเชื้อในประเทศ')
    else:
        r = requests.get(url = 'https://disease.sh/v3/covid-19/countries/'+arg)
        response = r.json()
        if ("message" in response) : return await ctx.send(response['message'])
        print(response)
        datestr = datetime.fromtimestamp(response["updated"] / 1e3)
        embedVar = discord.Embed(title=f':flag_{response["countryInfo"]["iso2"].lower()}: {response["country"]}', description=datestr.strftime("%A %d/%m/%Y, %H:%M:%S"), color=0x00ff00)
        embedVar.add_field(name=":thermometer_face:ผู้ป่วยทั้งหมด", value='{:,}'.format(response["cases"]), inline=True)
        embedVar.add_field(name=":mask:ผู้ป่วยวันนี้", value='{:,}'.format(response["todayCases"]), inline=True)
        embedVar.add_field(name=":skull:เสียชีวิตทั้งหมด", value='{:,}'.format(response["deaths"]), inline=True)
        embedVar.add_field(name=":skull_crossbones:เสียชีวิตวันนี้", value='{:,}'.format(response["todayDeaths"]), inline=True)
        embedVar.add_field(name=":mechanical_arm:รักษาหายทั้งหมด", value='{:,}'.format(response["recovered"]), inline=True)
        embedVar.add_field(name=":muscle:รักษาหายวันนี้", value='{:,}'.format(response["todayRecovered"]), inline=True)
        embedVar.add_field(name=":hospital:รักษาตัวในโรงพยาบาล", value='{:,}'.format(response["active"]), inline=True)
        embedVar.set_footer(text="beta test bot code by Isabella#3446")

        await ctx.send(embed=embedVar)        

@client.command()
async def all(ctx):
    r = requests.get(url = 'https://disease.sh/v3/covid-19/all') 
    response = r.json()
    print(response)
    datestr = datetime.fromtimestamp(response["updated"] / 1e3)
    embedVar = discord.Embed(title=':map: ' +'worldwide'+':syringe:', description=datestr.strftime("Last update %A %d/%m/%Y, %H:%M:%S") , color=0x00ff00)
    embedVar.add_field(name=":thermometer_face:ผู้ป่วยทั้งหมด", value='{:,}'.format(response["cases"]), inline=True)
    embedVar.add_field(name=":mask:ผู้ป่วยวันนี้", value='{:,}'.format(response["todayCases"]), inline=True)
    embedVar.add_field(name=":skull:เสียชีวิตทั้งหมด", value='{:,}'.format(response["deaths"]), inline=True)
    embedVar.add_field(name=":skull_crossbones:เสียชีวิตวันนี้", value='{:,}'.format(response["todayDeaths"]), inline=True)
    embedVar.add_field(name=":mechanical_arm:รักษาหายทั้งหมด", value='{:,}'.format(response["recovered"]), inline=True)
    embedVar.add_field(name=":muscle:รักษาหายวันนี้", value='{:,}'.format(response["todayRecovered"]), inline=True)
    embedVar.add_field(name=":hospital:รักษาตัวในโรงพยาบาล", value='{:,}'.format(response["active"]), inline=True)
    embedVar.set_footer(text="beta test bot code by Isabella#3446")

    await ctx.send(embed=embedVar)


@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat/')
      catjson = await request.json()

    embed = discord.Embed(title=":cat:Cat!", color=discord.Color.purple())
    embed.set_image(url=catjson['link'])
    embed.set_footer(text="beta test bot code by Isabella#3446")
    await ctx.send(embed=embed)


@client.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json() 
   embed = discord.Embed(title=":dog:Doggo!", color=discord.Color.purple()) 
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text="beta test bot code by Isabella#3446") 
   await ctx.send(embed=embed)

@client.command()
async def redpanda(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/red_panda')
      dogjson = await request.json() 
   embed = discord.Embed(title=":panda_face:Red Panda!", color=discord.Color.purple()) 
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text="beta test bot code by Isabella#3446") 
   await ctx.send(embed=embed)

@client.command()
async def panda(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/panda')
      dogjson = await request.json() 
   embed = discord.Embed(title=":panda_face:Panda!", color=discord.Color.purple()) 
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text="beta test bot code by Isabella#3446") 
   await ctx.send(embed=embed)



client.run(TOKEN)
