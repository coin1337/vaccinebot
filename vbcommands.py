import discord
import pandas as pd
from discord import Embed
import bs4
import requests
import lxml

def data(state):
  # Source: 'https://www.nytimes.com/interactive/2020/us/covid-19-vaccine-doses.html'
  data = pd.read_csv('data/vaccinedata.csv', index_col=0)
  statedata = data.loc[f'{state}']
  embed = discord.Embed(
    title = f"{state} Data:",
    description = statedata.to_string(), 
    color = 0xe67e22
  )
  return embed

def find(zipcode):
  data = pd.read_csv('data/vaccinefind.csv', index_col=0)
  try:
    zipcodedata = data.loc['z' + f'{zipcode}'].to_string()
  except Exception:
    zipcodedata = 'Center not found for this zipcode. Please use the .website command and click the link. Enter your zipcode on the Vaccine Finder website.'
  embed = discord.Embed(
    title = f'Closest Vaccine to {zipcode}:',
    description = zipcodedata,
    color = 0xe67e22
  )
  return embed

def links():
  embed = discord.Embed(
    title = "Useful Links",
    description = '''
    https://www.worldometers.info/coronavirus/#countries
    https://www.cdc.gov/vaccines/covid-19/reporting/vaccinefinder/about.html
    https://vaccinefinder.org/search/
    ''',
    color = 0xe67e22
    )
  
  return embed

def bot_help():
  embed = Embed(
                title = "VaccineBot Commands (>)",
                description = '''
                >vbhelp --> Returns list of bot commands.
                >links --> Returns useful links on vaccines/COVID-19.
                >data [state] --> Returns vaccine data for a US state.
                >info [vaccine] --> Returns info about three major vaccines: "pfizer", "moderna", and "johnson"
                >find [zipcode] --> Returns the nearest vaccine center to your zipcode.
                >vaccinate [user] --> Gives Vaccinated role to user. (ADMIN ONLY)
                ''',
                color = 0xe67e22
            )
  return embed

def vaccinate(ctx, member: discord.Member):
  if ctx.message.author.guild_permissions.administrator:
    text = "{0.name} was vaccinated!".format(member)
  else:
    text = "You do not have permission!"

  embed = discord.Embed(
    title = "Vaccinated Badge",
    description = text,
    color = 0xe67e22
  )

  return embed  

def info(vac):
  vac_dict = {
    'pfizer':'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/Pfizer-BioNTech.html',
    'moderna':'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/Moderna.html',
    'johnson':'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/janssen.html'
  }
  
  if vac.lower() in vac_dict.keys():
    res = requests.get(vac_dict[vac])
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    information = soup.select('.col-md-12.splash-col')[0].getText() + f'\nSource: {vac_dict[vac]}'
  else:
    information = f'No info found for "{vac}"– Did you misspell?\nThe three options are: "pfizer", "moderna", and "johnson"'
    
  embed = discord.Embed(
    title = f"{vac.capitalize()} Vaccine Info:",
    description = information,
    color = 0xe67e22
  )
  return embed
