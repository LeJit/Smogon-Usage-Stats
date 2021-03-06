#!/usr/bin/python

import string
import json
import math
from TA import *
import cgi, cgitb
form = cgi.FieldStorage() 

def keyify(s):
	sout = ''
	for c in s:
		if c in string.uppercase:
			sout = sout + c.lower()
		elif c in string.lowercase + '1234567890':
			sout = sout + c
	return sout

statTranslate = {'HP': 'hp',
		'Atk': 'atk',
		'Def': 'def',
		'SAtk': 'spa',
		'SDef': 'spd',
		'Spd': 'spe',
		'Spe': 'spe'}

aliases={
	'NidoranF': ['Nidoran-F'],
	'NidoranM': ['Nidoran-M'],
	'Pichu': ['Spiky Pichu'],
	'Rotom-Mow': ['Rotom-C'],
	'Rotom-Heat': ['Rotom-H'],
	'Rotom-Frost': ['Rotom-F'],
	'Rotom-Wash': ['Rotom-W'],
	'Rotom-Fan': ['Rotom-S'],
	'Deoxys-Attack': ['Deoxys-A'],
	'Deoxys-Defense': ['Deoxys-D'],
	'Deoxys-Speed': ['Deoxys-S'],
	'Wormadam-Sandy': ['Wormadam-G'],
	'Wormadam-Trash': ['Wormadam-S'],
	'Shaymin-Sky': ['Shaymin-S'],
	'Giratina-Origin': ['Giratina-O'],
	'Unown': ['Unown-B','Unown-C','Unown-D','Unown-E','Unown-F','Unown-G','Unown-H','Unown-I','Unown-J','Unown-K','Unown-L','Unown-M','Unown-N','Unown-O','Unown-P','Unown-Q','Unown-R','Unown-S','Unown-T','Unown-U','Unown-V','Unown-W','Unown-X','Unown-Y','Unown-Z','Unown-!','Unown-?'],
	'Burmy': ['Burmy-G','Burmy-S'],
	'Castform': ['Castform-Snowy','Castform-Rainy','Castform-Sunny'],
	'Cherrim': ['Cherrim-Sunshine'],
	'Shellos': ['Shellos-East'],
	'Gastrodon': ['Gastrodon-East'],
	'Deerling': ['Deerling-Summer','Deerling-Autumn','Deerling-Winter'],
	'Sawsbuck': ['Sawsbuck-Summer','Sawsbuck-Autumn','Sawsbuck-Winter'],
	'Tornadus-Therian': ['Tornadus-T'],
	'Thundurus-Therian': ['Thundurus-T'],
	'Landorus-Therian': ['Landorus-T'],
	'Keldeo': ['Keldeo-R','Keldeo-Resolution'],
	'Meloetta': ['Meloetta-S','Meloetta-Pirouette'],
	'Genesect': ['Genesect-Douse','Genesect-Burn','Genesect-Shock','Genesect-Chill','Genesect-D','Genesect-S','Genesect-B','Genesect-C'],
	'Darmanitan': ['Darmanitan-D','Darmanitan-Zen'],
	'Basculin': ['Basculin-Blue-Striped','Basculin-A'],
	'Kyurem-Black': ['Kyurem-B'],
	'Kyurem-White': ['Kyurem-W']
}

#fix species
replacements = {
	'Rotom-H' : 'Rotom-Heat',
	'Rotom-W' : 'Rotom-Wash',
	'Rotom-F' : 'Rotom-Frost',
	'Rotom-S' : 'Rotom-Fan',
	'Rotom-C' : 'Rotom-Mow',
	'Rotom- H' : 'Rotom-Heat',
	'Rotom- W' : 'Rotom-Wash',
	'Rotom- F' : 'Rotom-Frost',
	'Rotom- S' : 'Rotom-Fan',
	'Rotom- C' : 'Rotom-Mow',
	'Rotom-h' : 'Rotom-Heat',
	'Rotom-w' : 'Rotom-Wash',
	'Rotom-f' : 'Rotom-Frost',
	'Rotom-s' : 'Rotom-Fan',
	'Rotom-c' : 'Rotom-Mow',
	'Tornadus-T' : 'Tornadus-Therian',
	'Thundurus-T' : 'Thundurus-Therian',
	'Landorus-T' : 'Landorus-Therian',
	'Deoxys-D' : 'Deoxys-Defense',
	'Deoxys-A' : 'Deoxys-Attack',
	'Deoxys-S' : 'Deoxys-Speed',
	'Kyurem-B' : 'Kyurem-Black',
	'Kyurem-W' : 'Kyurem-White',
	'Shaymin-S' : 'Shaymin-Sky',
	'Ho-oh' : 'Ho-Oh',
	"Birijion": "Virizion",
	"Terakion": "Terrakion",
	"Agirudaa": "Accelgor",
	"Randorosu": "Landorus",
	"Urugamosu": "Volcarona",
	"Erufuun": "Whimsicott",
	"Doryuuzu": "Excadrill",
	"Burungeru": "Jellicent",
	"Nattorei": "Ferrothorn",
	"Shandera": "Chandelure",
	"Roobushin": "Conkeldurr",
	"Ononokusu": "Haxorus",
	"Sazandora": "Hydreigon",
	"Chirachiino": "Cinccino",
	"Kyuremu": "Kyurem",
	"Jarooda": "Serperior",
	"Zoroaaku": "Zoroark",
	"Shinboraa": "Sigilyph",
	"Barujiina": "Mandibuzz",
	"Rankurusu": "Reuniclus",
	"Borutorosu": "Thundurus",
	"Mime Jr" : "Mime Jr.", #this one's my fault
	#to be fair, I never observed the following, but better safe than sorry
	'Giratina-O' : 'Giratina-Origin',
	'Keldeo-R' : 'Keldeo-Resolution',
	'Wormadam-G' : 'Wormadam-Sandy',
	'Wormadam-S' : 'Wormadam-Trash',
	"Dnite": "Dragonite",
	"Ferry": "Ferrothorn",
	"Forry": "Forretress",
	"Luke":  "Lucario",
	"P2": "Porygon2",
	"Pory2": "Porygon2",
	"Pz": "Porygon-Z",
	"Poryz": "Porygon-Z",
	"Rank": "Reuniclus",
	"Ttar": "Tyranitar"
}


raw = str(form.getvalue('team')).split('\r\n')
for i in range(len(raw)):
	raw[i]=raw[i]+'\n'

team = []
speciesNextLine = True
species = 'empty'
item = 'nothing'
ability = ''
level=100
evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}
moves = []
for line in raw:
	if line == '\n':
		if species != 'empty':
			team.append({
				'species': species,
				'item': item,
				'ability': ability,
				'nature': nature,
				'level': level,
				'evs': evs, #gotta be careful with this, bc it's pointing, not copying
				'ivs': ivs, #   "
				'moves': moves# "
					})
			#reset everything
			species = 'empty'
			item = 'nothing'
			ability = ''
			level=100
			for stat in evs.keys():
				evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
				ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}
			moves = []
		speciesNextLine = True
		
		continue
	if speciesNextLine:
		speciesNextLine = False
		if '(' in line: #nicknamed
			species = keyify(line[string.rfind(line,'(')+1:string.rfind(line,')')])
			if species in ['m','f']: #you got gender, nto species
				if '(' in line[:string.rfind(line,'(')]:
					species = line[string.rfind(line,'(',0,string.rfind(line,'('))+1:string.rfind(line,')',0,string.rfind(line,'('))]
				else:
					species = line[:string.rfind(line,'(')]
		else:
			if '@' in line: #is there an item
				species = line[0:string.rfind(line,'@')]
			else:
				species = line[0:len(line)-1]
		if species[0] not in string.lowercase + string.uppercase:
			species=species[1:]
		while species[len(species)-1] in ')". ':
			species=species[:len(species)-1]
		if species[0] in string.lowercase or species[1] in string.uppercase:
			species = species.title()
		if species in replacements.keys():
			species = replacements[species]

		for s in aliases: #combine appearance-only variations and weird PS quirks
			if species in aliases[s]:
				species = s
				break
		species = keyify(species)
		if '@' in line:
			item = keyify(line[string.rfind(line,'@')+1:len(line)-1])
	elif line.startswith('Trait:'):
		ability = keyify(line[6:len(line)-1])
	elif line.startswith('Level:'):
		level = int(line[6:len(line)-1])
	elif line.startswith('EVs') or line.startswith('IVs'):
		mods = line[4:len(line)-1].split('/')
		for mod in mods:
			while mod[0] == ' ':
				mod=mod[1:]
			while mod[len(mod)-1] == ' ':
				mod=mod[:len(mod)-1]
			num=mod[:string.find(mod,' ')]
			stat=statTranslate[mod[len(num)+1:]]
			if line.startswith('EVs'):
				evs[stat]=int(num)
			else:
				ivs[stat]=int(num)
	elif line.startswith('Nature'):
		nature = keyify(line[7:string.rfind(line,'(')-1])
	elif line[0] == '-':
		moves.append(keyify(line[1:len(line)-1]))
	elif not line.startswith('Shiny'): #nature
		nature = keyify(line[0:string.rfind(line,'ature')-2])#Nature/nature
if not speciesNextLine:
	team.append({
		'species': species,
		'item': item,
		'ability': ability,
		'nature': nature,
		'level': level,
		'evs': evs,
		'ivs': ivs,
		'moves': moves})

analysis = analyzeTeam(team)
bias = analysis['bias']
stalliness = analysis['stalliness']
tags = analysis['tags']

tko = math.pow(2.0,stalliness)*3

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Results</title>"
print "</head>"
print "<body>"
print "Bias: %d <br/>" % (bias)
print "Stalliness: %f (%3.2f T/KO)<br/>" %(stalliness,tko)
print "Tags: %s<br/>"%str(tags)
print "To find out more, check out <a href=http://pokemetrics.wordpress.com>http://pokemetrics.wordpress.com</a>"
print "</body>"
print "</html>"

