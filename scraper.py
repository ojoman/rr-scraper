import json
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
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
browser.get("https://dex.radicalred.net/")
time.sleep(2)

SCROLL_PAUSE_TIME = 0.1

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


mons = browser.find_elements_by_class_name("speciesNameWrapper")
allMons = list(map(lambda n: n.text, mons))


#reloading stopped the data from being weird and stale
browser.get("https://dex.radicalred.net/")
time.sleep(2)
search_input = browser.find_element_by_id("speciesFilterInput")
file = open("./pokemon-data/data.csv", 'w')

for name in allMons:
  search_input.clear()
  search_input.send_keys(name)
  search_input.send_keys(Keys.RETURN)
  time.sleep(0.4)
  block = browser.find_element_by_id("speciesModal")
  stuff = block.find_element_by_id("speciesPanelInfoDisplay")
  
  number = stuff.find_element_by_class_name("infoDexIDWrapper").text
  if "#" in number:
    number = number.replace("#", "")
  
  sprite = stuff.find_element_by_class_name("infoSprite").get_attribute("src")
  
  types = stuff.find_element_by_class_name("infoTypesWrapper").find_elements_by_class_name("typeWrapper")
  type1 = types[0].text.capitalize()
  if len(types) > 1:
    type2 = types[1].text.capitalize()
  else:
    type2 = 'none'
  abilitys = stuff.find_element_by_class_name("infoAbilitiesWrapper")
  try:
    ability1 = abilitys.find_element_by_class_name("infoAbilitiesPrimary").text.split("-")[0].capitalize()
  except:
    ability1 = 'none'
    
  try:
    ability2 = abilitys.find_element_by_class_name("infoAbilitiesSecondary").text.split("-")[0].capitalize()
  except:
    ability2 = 'none'
  
  try:
    ability3 = abilitys.find_element_by_class_name("infoAbilitiesHidden").text.split("-")[0].capitalize()
  except:
    ability3 = 'none'
  
  stats = stuff.find_elements_by_class_name("infoStatValue")
  
  hp = stats[0].text
  attack = stats[1].text
  defense = stats[2].text
  special_atk = stats[3].text
  special_def = stats[4].text
  speed = stats[5].text
  
  moveArea = browser.find_element_by_id("speciesPanelLearnsets")
  moves = moveArea.find_elements_by_class_name("moveNameWrapper")
  moves = list(map(lambda n: n.text, moves))
  
  movelist = "#"
  try:
    if len(moves) > 0:
      for move in moves:
        if "#" + move + "#" not in movelist:
          movelist += move
          movelist += "#"
    else:
      movelist = ''
  except:
      movelist = ''
  
  #print(movelist)
  
  file.write(number + "," + 
    name + "," + 
    "sprite" + "," + 
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
  
  
  try:
    block.send_keys(Keys.ESCAPE)
    #print("success")
    time.sleep(0.4)
  except:
    print("angry")
  print(name)
  #print(number + " " + name + " " + type1 + " " + type2 + " " + ability1 + " " + ability2 + " " + ability3)

browser.close()
file.close()
