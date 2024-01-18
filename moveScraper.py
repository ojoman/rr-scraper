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
browser.get("https://dex.pokemonshowdown.com/moves/")

#this is wet garbage but i'm only running it once so you can fix it
def getElements():
  moves = browser.find_elements_by_class_name("movenamecol")
  ActionChains(browser)\
  .move_to_element(moves[len(moves) - 1])\
  .perform()
  return moves

#i love variables
prevMove = "a"
newMove = "b"
allMoves = []
file = open("./pokemon-data/moves.csv", 'w')
while not(prevMove == newMove):
  prevMove = newMove
  allMoves = getElements()
  newMove = allMoves[len(allMoves) - 1].text
  
allMoves = list(map(lambda n: n.text, allMoves))

#reloading stopped the data from being weird and stale
browser.get("https://dex.pokemonshowdown.com/moves/")
search_input = browser.find_element_by_class_name("searchbox")

for name in allMoves:
  search_input.clear()
  search_input.send_keys(name)
  search_input.send_keys(Keys.RETURN)
    
  print(name)
  types = browser.find_element_by_class_name("movetypeentry").find_elements_by_class_name("type")
  if not types[1].text == "STATUS":
    basePower = browser.find_element_by_class_name("powerentry").find_element_by_tag_name("strong").text
  else:
    basePower = "n/a"
  accuracy = browser.find_element_by_class_name("accuracyentry").find_element_by_tag_name("dd").text
  pp = browser.find_element_by_class_name("ppentry").find_element_by_tag_name("dd")
  pp = pp.text.split("\n")
  if len(pp) == 1:
    pp = pp[0]
  else:
    minPP = pp[0]
    maxPP = pp[1]
    maxPP = maxPP.replace("(max: ", "")
    maxPP = maxPP.replace(")", "")
    pp = minPP + "-" + maxPP


  
  desc = "\"" + browser.find_element_by_tag_name("p").text + "\""
  name = "\"" + name + "\""

  file.write(name + "," +
    types[0].text.capitalize() + "," +
    types[1].text.capitalize() + "," +
    basePower + "," +
    accuracy + "," +
    pp + "," +
    desc + "\n")
  
  
browser.close()
file.close()
