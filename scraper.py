import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.set_window_size(1080,800)
browser.get("https://dex.pokemonshowdown.com/pokemon/")
search_input = browser.find_element_by_class_name("searchbox")

file = open("./pokemon-data/pokemon-gen1-data.csv", 'w')
file.write("Pokemon, Number, Type1, Type2, Ability1, Ability2, Ability3, HP, Attack, Defense, Sp. Atk, Sp. Def, Speed, Sprite\n")

with open('./names.json') as f:
  pokemon_names = json.loads(f.read())

for name in pokemon_names[0:151]:
  search_input.clear()
  search_input.send_keys(name)
  search_input.send_keys(Keys.RETURN)

  pokemon = name
  number = browser.find_element_by_tag_name("code").text.replace("#", "")
  
  moves = browser.find_elements_by_class_name("shortmovenamecol")
  movelist = "#"
  for move in moves:
  	if "#" + move.text + "#" not in movelist:
	  	movelist += move.text
	  	movelist += "#"
      
  file.write(pokemon + "," + number 
    + "," + movelist + "\n")
  print(number)

browser.close()
file.close()




