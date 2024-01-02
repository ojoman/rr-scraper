import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains



browser = webdriver.Chrome(ChromeDriverManager().install())
browser.set_window_size(1080,800)
browser.get("https://dex.pokemonshowdown.com/pokemon/")

def getElements():
  mons = browser.find_elements_by_class_name("pokemonnamecol")
  ActionChains(browser)\
  .move_to_element(mons[len(mons) - 1])\
  .perform()
  return mons

prevMon = "a"
newMon = "b"
allMons = []
file = open("./pokemon-data/pokemon-gen1-data.csv", 'w')
file.write("Pokemon, Number, Moves\n")
while not(prevMon == newMon):
  prevMon = newMon
  allMons = list(map(lambda n: n.text, getElements()))
  newMon = allMons[len(allMons) - 1]
  
browser.get("https://dex.pokemonshowdown.com/pokemon/")
search_input = browser.find_element_by_class_name("searchbox")

for name in allMons:
  search_input.clear()
  search_input.send_keys(name)
  search_input.send_keys(Keys.RETURN)

  number = browser.find_element_by_tag_name("code").text.replace("#", "")
  
  moves = browser.find_elements_by_class_name("shortmovenamecol")
  movelist = "#"
  for move in moves:
    if "#" + move.text + "#" not in movelist:
      movelist += move.text
      movelist += "#"
      
  file.write(name + "," + number 
    + "," + movelist + "\n")
  print(number)

browser.close()
file.close()
