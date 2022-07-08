import json
import requests
import discord
from discord.ext import commands
from playsound import playsound
import asyncio
import datetime

client = commands.Bot()


@client.event
async def on_ready():
    playsound('nuiba.mp3')
    await checkPack()


async def checkPack():
    f = open("parcels.json", 'r')
    packages = json.load(f)
    f.close()
    for key in packages['parcels']:
        try:
            print(key)
            r = requests.get(
                f'https://mano.omniva.lt/api/track/shipment/{key}')
            info = r.json()
            print(info)
            print(info['states'][len(info['states']) - 1]['location']['locationName'])
            print(packages['parcels'][key]['stateLocation'])
            print(packages['parcels'][key]['state'])
            print(info['states'][len(info['states']) - 1]['stateName'])
            if (info['states'][len(info['states']) - 1]['stateName'] != packages['parcels'][key]['state']) or (info['states'][len(info['states']) - 1]['location']['locationName'] != packages['parcels'][key]['stateLocation']):
                packages['parcels'][key]['state'] = info['states'][len(info['states']) - 1]['stateName']
                packages['parcels'][key]['stateLocation'] = info['states'][len(info['states']) - 1]['location']['locationName']
                datetims = datetime.datetime.strptime(
                    info['states'][len(info['states']) - 1]['stateDate'], "%Y-%m-%dT%H:%M:%S.%f") + datetime.timedelta(hours=3)
                packages['parcels'][key]['time'] = datetims.strftime(
                    "%m/%d/%Y, %H:%M:%S")
                await client.get_guild(774318024269889586).system_channel.send(f"<@551503912109342720> Hey, there is a new parcel update!\n**{packages['parcels'][key]['nickname']} / {info['states'][len(info['states']) - 1]['stateName']} | {datetims.strftime('%m/%d/%Y, %H:%M:%S')} `{info['states'][len(info['states']) - 1]['location']['locationName'].replace('Antarktidos Pastomatas', 'Haha! You know!')}`**")
                x = open("parcels.json", 'w')
                json.dump(packages, x, indent=4)
                x.close()
                playsound('Soviet union\'s anthem (slowed+ sad version).mp4.mp3')
        except:
            print('erorr')

    await asyncio.sleep(60)
    await checkPack()


@client.slash_command()
async def add(ctx: discord.ApplicationContext, track: str, nickname: str):
    if (ctx.user.id != 551503912109342720):
        return
    with open("parcels.json", 'r') as f:
        packages = json.load(f)
        packages['parcels'][track] = {}
        packages['parcels'][track]['nickname'] = nickname
        packages['parcels'][track]['state'] = 'niga'
        packages['parcels'][track]['stateLocation'] = 'nige'
        packages['parcels'][track]['time'] = 'none'
        with open("parcels.json", 'w') as r:
            json.dump(packages, r, indent=4)
            await ctx.respond('Added! 😄')

with open("token.txt", 'r') as f:
    client.run(f.read())
