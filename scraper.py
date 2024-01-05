import json
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 800)) 
display.start()

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()

options = [
  "--window-size=1200,1200",
  "--ignore-certificate-errors"
  
  ]

for option in options:
  chrome_options.add_argument(option)


browser = webdriver.Chrome(options = chrome_options)

#wider window required for dual screen operation
browser.set_window_size(1200,800)
browser.get("https://dex.pokemonshowdown.com/pokemon/")

#this is wet garbage but i'm only running it once so you can fix it
def getElements():
  mons = browser.find_elements_by_class_name("pokemonnamecol")
  ActionChains(browser)\
  .move_to_element(mons[len(mons) - 1])\
  .perform()
  return mons

#i love variables
prevMon = "a"
newMon = "b"
allMons = []
file = open("./pokemon-data/data.csv", 'w')
while not(prevMon == newMon):
  prevMon = newMon
  allMons = getElements()
  newMon = allMons[len(allMons) - 1].text
  
allMons = list(map(lambda n: n.text, allMons))

#reloading stopped the data from being weird and stale
browser.get("https://dex.pokemonshowdown.com/pokemon/")
search_input = browser.find_element_by_class_name("searchbox")

for name in allMons:
  search_input.clear()
  search_input.send_keys(name)
  search_input.send_keys(Keys.RETURN)
  
  #non-standard mons are sorted by tier, which is generally CAP or Illegal
  try:
    number = browser.find_element_by_tag_name("code").text
  except:
    number = browser.find_element_by_class_name("tier").text
  
  
  #CAP, illegal, pokestar etc
  if "#" in number:
    number = number.replace("#", "")
  
  types = browser.find_elements_by_class_name("type")
  type1 = types[0].text.capitalize()
  if len(types) == 2:
    type2 = types[1].text.capitalize()
  else:
    type2 = 'none'

  #some mons (just missingno tbh) have no abilities
  try:
    abilities = browser.find_elements_by_css_selector("dd.imgentry > a")
    ability1 = abilities[0].text
    if len(abilities) >= 2:
      ability2 = abilities[1].text
    else:
      ability2 = 'none'

    if len(abilities) == 3:
      ability3 = abilities[2].text
    else:
      ability3 = 'none'
  except:
    ability1 = 'none'
    ability2 = 'none'
    ability3 = 'none'
  

  base_stats = browser.find_elements_by_class_name('stat')
  hp = base_stats[0].text
  attack = base_stats[1].text
  defense = base_stats[2].text
  special_atk = base_stats[3].text
  special_def = base_stats[4].text
  speed = base_stats[5].text
  
  sprite = browser.find_element_by_class_name("sprite").get_attribute("src")
  
  #moves are separated by '#' with a bonus '#' on the start and end so i can regex match them
  
  moves = browser.find_elements_by_class_name("shortmovenamecol")
  movelist = "#"
  try:
    if len(moves) > 0:
      for move in moves:
        if "#" + move.text + "#" not in movelist:
          movelist += move.text
          movelist += "#"
    else:
      movelist = ''
  except:
      movelist = ''
      
  #changed the order slightly compared to the original since i'm using this in place of a dex
  #i had been using in the past and wanted them to be compatible
  file.write(number + "," + 
    name + "," + 
    sprite + "," + 
    type1 + "," + 
    type2 + "," + 
    ability1 + "," + 
    ability2 + "," + 
    ability3 + "," + 
    hp + "," + 
    attack + "," + 
    defense + "," + 
    special_atk + "," + 
    special_def + "," + 
    speed + "," + 
    movelist + "\n")
  print(number)

browser.close()
file.close()
