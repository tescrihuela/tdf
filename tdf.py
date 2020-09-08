import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv

file = 'ranking.csv'

class_general = u"https://tourdefrance2020.fr/classement-general/"
class_montagne = u"https://tourdefrance2020.fr/classement-du-meilleur-grimpeur/"
class_points = u"https://tourdefrance2020.fr/classement-par-points/"
class_jeune = u"https://tourdefrance2020.fr/classement-du-meilleur-jeune/"

fantasy = {
    "general": [50, 45, 40, 35, 30, 28, 26, 24, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10,10,10,10,10, 9,9,9,9,9, 8,8,8,8,8, 7,7,7,7,7, 6,6,6,6,6, 5,5,5,5,5, 4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3,3,3,3,3, 2,2,2,2,2,2,2,2,2,2, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    "montagne": [30, 26, 22, 20, 18, 16, 14 ,12, 10, 8, 6, 4, 3, 2, 1],
    "points": [30, 26, 22, 20, 18, 16, 14 ,12, 10, 8, 6, 4, 3, 2, 1],
    "jeune": [20, 18, 16, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
}

fantasy_etape = {
	"etape": [200, 150, 120, 100, 90, 80, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 9, 8,8,8,8,8, 7,7,7,7,7, 6,6,6,6,6, 5,5,5,5,5, 4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3,3,3,3,3, 2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
}

coureurs = {
	'Adam Yates': {
		'equipe': 'Mitchelton-Scott',                               
		'cout': 16,
	},
	'Alberto Bettiol': {
		'equipe': 'EF Pro Cycling',                               
		'cout': 11,
	},
	'Alejandro Valverde': {
		'equipe': 'Movistar',                             
		'cout': 17,
	},
	'Alessandro De Marchi': {
		'equipe': 'CCC',
		'cout': 8,
	},
	'Alexander Kristoff': {
		'equipe': 'UAE Emirates',
		'cout': 17,
	},
	'Alexey Lutsenko': {
		'equipe': 'Astana',
		'cout': 14,
	},
	'Alexis Vuillermoz': {
		'equipe': 'AG2R La Mondiale',
		'cout': 9,
	},
	'Amund Grøndahl Jansen': {
		'equipe': 'Jumbo-Visma',
		'cout': 6,
	},
	'Andrey Amador': {
		'equipe': 'Ineos Grenadiers',
		'cout': 9,
	},
	'André Greipel': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 11,
	},
	'Anthony Turgis': {
		'equipe': 'Total Direct Energie',
		'cout': 8,
	},
	'Bauke Mollema': {
		'equipe': 'Trek-Segafredo',
		'cout': 16,
	},
	'Ben Hermans': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 12,
	},
	'Benoît Cosnefroy': {
		'equipe': 'AG2R La Mondiale',
		'cout': 8,
	},
	'Bob Jungels': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 12,
	},
	'Bryan Coquard': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 13,
	},
	'Caleb Ewan': {
		'equipe': 'Lotto-Soudal',
		'cout': 20,
	},
	'Carlos Verona': {
		'equipe': 'Movistar',
		'cout': 8,
	},
	'Casper Pederse': {
		'equipe': 'Sunweb',
		'cout': 6,
	},
	'Cees Bol': {
		'equipe': 'Sunweb',
		'cout': 10,
	},
	'Christophe Laporte': {
		'equipe': 'Cofidis',
		'cout': 13,
	},
	'Christopher Juul Jensen': {
		'equipe': 'Mitchelton-Scott',
		'cout': 7,
	},
	'Clément Russo': {
		'equipe': 'Arkea-Samsic',
		'cout': 6,
	},
	'Clément Venturini': {
		'equipe': 'AG2R La Mondiale',
		'cout': 9,
	},
	'Connor Swift': {
		'equipe': 'Arkea-Samsic',
		'cout': 8,
	},
	'Cyril Barthe': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 8,
	},
	'Cyril Gautier': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 8,
	},
	'Damiano Caruso': {
		'equipe': 'Bahrain-McLaren',
		'cout': 12,
	},
	'Dan Martin': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 16,
	},
	'Daniel Martinez': {
		'equipe': 'EF Pro Cycling',
		'cout': 19,
	},
	'Daniel Oss': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 6,
	},
	'Dario Cataldo': {
		'equipe': 'Movistar',
		'cout': 9,
	},
	'Daryl Impey': {
		'equipe': 'Mitchelton-Scott',
		'cout': 11,
	},
	'David De La Cruz': {
		'equipe': 'UAE Emirates',
		'cout': 13,
	},
	'David Gaudu': {
		'equipe': 'Groupama-FDJ',
		'cout': 14,
	},
	'Davide Formolo': {
		'equipe': 'UAE Emirates',
		'cout': 13,
	},
	'Dayer Quintana': {
		'equipe': 'Arkea-Samsic',
		'cout': 8,
	},
	'Domenico Pozzovivo': {
		'equipe': 'NTT',
		'cout': 11,
	},
	'Dries Devenyns': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 6,
	},
	'Dylan Van Baarle': {
		'equipe': 'Ineos Grenadiers',
		'cout': 12,
	},
	'Edvald Boasson Hagen': {
		'equipe': 'NTT',
		'cout': 13,
	},
	'Edward Theuns': {
		'equipe': 'Trek-Segafredo',
		'cout': 6,
	},
	'Egan Bernal': {
		'equipe': 'Ineos Grenadiers',
		'cout': 21,
	},
	'Elia Viviani': {
		'equipe': 'Cofidis',
		'cout': 18,
	},
	'Emanuel Buchmann': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 18,
	},
	'Enric Mas': {
		'equipe': 'Movistar',
		'cout': 14,
	},
	'Esteban Chaves': {
		'equipe': 'Mitchelton-Scott',
		'cout': 14,
	},
	'Fabien Grellier': {
		'equipe': 'Total Direct Energie',
		'cout': 6,
	},
	'Felix Großschartner': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 12,
	},
	'Frederick Frison': {
		'equipe': 'Lotto-Soudal',
		'cout': 6,
	},
	'Geoffrey Soupe': {
		'equipe': 'Total Direct Energie',
		'cout': 6,
	},
	'George Bennett': {
		'equipe': 'Jumbo-Visma',
		'cout': 12,
	},
	'Gorka Izagirre': {
		'equipe': 'Astana',
		'cout': 11,
	},
	'Greg Van Avermaet': {
		'equipe': 'CCC',
		'cout': 16,
	},
	'Gregor Mühlberger': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 11,
	},
	'Guillaume Martin': {
		'equipe': 'Cofidis',
		'cout': 13,
	},
	'Guy Niv': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 6,
	},
	'Harold Tejada': {
		'equipe': 'Astana',
		'cout': 10,
	},
	'Hugh Carthy': {
		'equipe': 'EF Pro Cycling',
		'cout': 11,
	},
	'Hugo Hofstetter': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 10,
	},
	'Hugo Houle': {
		'equipe': 'Astana',
		'cout': 6,
	},
	'Ilnur Zakarin': {
		'equipe': 'CCC',
		'cout': 15,
	},
	'Imanol Erviti': {
		'equipe': 'Movistar',
		'cout': 6,
	},
	'Ion Izagirre': {
		'equipe': 'Astana',
		'cout': 14,
	},
	'Jack Bauer': {
		'equipe': 'Mitchelton-Scott',
		'cout': 6,
	},
	'Jan Hirt': {
		'equipe': 'CCC',
		'cout': 7,
	},
	'Jan Polanc': {
		'equipe': 'UAE Emirates',
		'cout': 10,
	},
	'Jasper De Buyst': {
		'equipe': 'Lotto-Soudal',
		'cout': 7,
	},
	'Jasper Stuyven': {
		'equipe': 'Trek-Segafredo',
		'cout': 13,
	},
	'Jens Debusschere': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 10,
	},
	'Jens Keukeleire': {
		'equipe': 'EF Pro Cycling',
		'cout': 9,
	},
	'Jesus Herrada': {
		'equipe': 'Cofidis',
		'cout': 12,
	},
	'Jonas Koch': {
		'equipe': 'CCC',
		'cout': 6,
	},
	'Jonathan Castroviejo': {
		'equipe': 'Ineos Grenadiers',
		'cout': 9,
	},
	'Joris Nieuwenhuis': {
		'equipe': 'Sunweb',
		'cout': 6,
	},
	'José Joaquín Rojas': {
		'equipe': 'Movistar',
		'cout': 8,
	},
	'Julian Alaphilippe': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 19,
	},
	'Jérôme Cousin': {
		'equipe': 'Total Direct Energie',
		'cout': 6,
	},
	'Kasper Asgreen': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 9,
	},
	'Kenny Elissonde': {
		'equipe': 'Trek-Segafredo',
		'cout': 9,
	},
	'Krists Neilands': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 9,
	},
	'Kévin Ledanois': {
		'equipe': 'Arkea-Samsic',
		'cout': 6,
	},
	'Kévin Reza': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 7,
	},
	'Lennard Kämna': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 9,
	},
	'Luis Leon Sanchez': {
		'equipe': 'Astana',
		'cout': 9,
	},
	'Luka Mezgec': {
		'equipe': 'Mitchelton-Scott',
		'cout': 10,
	},
	'Lukas Pöstlberger': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 6,
	},
	'Luke Rowe': {
		'equipe': 'Ineos Grenadiers',
		'cout': 6,
	},
	'Mads Pedersen': {
		'equipe': 'Trek-Segafredo',
		'cout': 13,
	},
	'Marc Hirschi': {
		'equipe': 'Sunweb',
		'cout': 13,
	},
	'Marc Soler': {
		'equipe': 'Movistar',
		'cout': 13,
	},
	'Marco Haller': {
		'equipe': 'Bahrain-McLaren',
		'cout': 8,
	},
	'Marco Marcato': {
		'equipe': 'UAE Emirates',
		'cout': 9,
	},
	'Matej Mohoric': {
		'equipe': 'Bahrain-McLaren',
		'cout': 10,
	},
	'Mathieu Burgaudeau': {
		'equipe': 'Total Direct Energie',
		'cout': 6,
	},
	'Matteo Trentin': {
		'equipe': 'CCC',
		'cout': 15,
	},
	'Matthieu Ladagnous': {
		'equipe': 'Groupama-FDJ',
		'cout': 6,
	},
	'Max Walscheid': {
		'equipe': 'NTT',
		'cout': 9,
	},
	'Maxime Chevalier': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 6,
	},
	'Maximilian Schachmann': {
		'equipe': 'Bora-Hansgrohe',
		'cout': 14,
	},
	'Michael Gogl': {
		'equipe': 'NTT',
		'cout': 7,
	},
	'Michael Morkov': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 6,
	},
	'Michael Schär': {
		'equipe': 'CCC',
		'cout': 6,
	},
	'Michael Valgren': {
		'equipe': 'NTT',
		'cout': 10,
	},
	'Michal Kwiatkowski': {
		'equipe': 'Ineos Grenadiers',
		'cout': 15,
	},
	'Miguel Angel Lopez': {
		'equipe': 'Astana',
		'cout': 19,
	},
	'Mikaël Cherel': {
		'equipe': 'AG2R La Mondiale',
		'cout': 7,
	},
	'Mikel Landa': {
		'equipe': 'Bahrain-McLaren',
		'cout': 19,
	},
	'Mikel Nieve': {
		'equipe': 'Mitchelton-Scott',
		'cout': 12,
	},
	'Nairo Quintana': {
		'equipe': 'Arkea-Samsic',
		'cout': 20,
	},
	'Nans Peters': {
		'equipe': 'AG2R La Mondiale',
		'cout': 8,
	},
	'Neilson Powless': {
		'equipe': 'EF Pro Cycling',
		'cout': 8,
	},
	'Nelson Oliveira': {
		'equipe': 'Movistar',
		'cout': 8,
	},
	'Niccolo Bonifazio': {
		'equipe': 'Total Direct Energie',
		'cout': 12,
	},
	'Nicolas Edet': {
		'equipe': 'Cofidis',
		'cout': 7,
	},
	'Nicolas Roche': {
		'equipe': 'Sunweb',
		'cout': 7,
	},
	'Nikias Arndt': {
		'equipe': 'Sunweb',
		'cout': 7,
	},
	'Niklas Eg': {
		'equipe': 'Trek-Segafredo',
		'cout': 8,
	},
	'Nils Politt': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 10,
	},
	'Oliver Naesen': {
		'equipe': 'AG2R La Mondiale',
		'cout': 11,
	},
	'Omar Fraile': {
		'equipe': 'Astana',
		'cout': 8,
	},
	'Pavel Sivakov': {
		'equipe': 'Ineos Grenadiers',
		'cout': 15,
	},
	'Pello Bilbao': {
		'equipe': 'Bahrain-McLaren',
		'cout': 12,
	},
	'Peter Sagan': {
		'equipe': 'Bora-Hansgroh',
		'cout': 19,
	},
	'Pierre Latour': {
		'equipe': 'AG2R La Mondiale',
		'cout': 12,
	},
	'Pierre Rolland': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 10,
	},
	'Pierre-Luc Périchon': {
		'equipe': 'Cofidis',
		'cout': 6,
	},
	'Primoz Roglic': {
		'equipe': 'Jumbo-Visma',
		'cout': 22,
	},
	'Quentin Pacher': {
		'equipe': 'B&B Hôtels-Vital Concept',
		'cout': 9,
	},
	'Richard Carapaz': {
		'equipe': 'Ineos Grenadiers',
		'cout': 19,
	},
	'Richie Porte': {
		'equipe': 'Trek-Segafredo',
		'cout': 16,
	},
	'Rigoberto Uran': {
		'equipe': 'EF Pro Cycling',
		'cout': 18,
	},
	'Robert Gesink': {
		'equipe': 'Jumbo-Visma',
		'cout': 9,
	},
	'Roger Kluge': {
		'equipe': 'Lotto-Soudal',
		'cout': 6,
	},
	'Romain Bardet': {
		'equipe': 'AG2R La Mondiale',
		'cout': 16,
	},
	'Romain Sicard': {
		'equipe': 'Total Direct Energie',
		'cout': 6,
	},
	'Roman Kreuziger': {
		'equipe': 'NTT',
		'cout': 8,
	},
	'Rudy Molard': {
		'equipe': 'Groupama-FDJ',
		'cout': 10,
	},
	'Ryan Gibbons': {
		'equipe': 'NTT',
		'cout': 9,
	},
	'Rémi Cavagna': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 10,
	},
	'Sam Bennett': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 20,
	},
	'Sam Bewley': {
		'equipe': 'Mitchelton-Scott',
		'cout': 6,
	},
	'Sepp Kuss': {
		'equipe': 'Jumbo-Visma',
		'cout': 14,
	},
	'Sergio Higuita': {
		'equipe': 'EF Pro Cycling',
		'cout': 16,
	},
	'Simon Geschke': {
		'equipe': 'CCC',
		'cout': 7,
	},
	'Simone Consonni': {
		'equipe': 'Cofidis',
		'cout': 9,
	},
	'Sonny Colbrelli': {
		'equipe': 'Bahrain-McLaren',
		'cout': 15,
	},
	'Stefan Küng': {
		'equipe': 'Groupama-FDJ',
		'cout': 9,
	},
	'Sébastien Reichenbach': {
		'equipe': 'Groupama-FDJ',
		'cout': 10,
	},
	'Søren Kragh Andersen': {
		'equipe': 'Sunweb',
		'cout': 11,
	},
	'Tadej Pogacar': {
		'equipe': 'UAE Emirates',
		'cout': 18,
	},
	'Tejay Van Garderen': {
		'equipe': 'EF Pro Cycling',
		'cout': 11,
	},
	'Thibaut Pinot': {
		'equipe': 'Groupama-FDJ',
		'cout': 20,
	},
	'Thomas De Gendt': {
		'equipe': 'Lotto-Soudal',
		'cout': 12,
	},
	'Tiesj Benoot': {
		'equipe': 'Sunweb',
		'cout': 16,
	},
	'Tim Declercq': {
		'equipe': 'Deceuninck-Quick-Step',
		'cout': 6,
	},
	'Tom Dumoulin': {
		'equipe': 'Jumbo-Visma',
		'cout': 19,
	},
	'Tom Van Asbroeck': {
		'equipe': 'Israël Start-Up Nation',
		'cout': 11,
	},
	'Toms Skujins': {
		'equipe': 'Trek-Segafredo',
		'cout': 8,
	},
	'Tony Martin': {
		'equipe': 'Jumbo-Visma',
		'cout': 7,
	},
	'Valentin Madouas': {
		'equipe': 'Groupama-FDJ',
		'cout': 10,
	},
	'Vegard Stake Laengen': {
		'equipe': 'UAE Emirates',
		'cout': 6,
	},
	'Warren Barguil': {
		'equipe': 'Arkea-Samsic',
		'cout': 14,
	},
	'Winner Anacona': {
		'equipe': 'Arkea-Samsic',
		'cout': 9,
	},
	'Wout Poels': {
		'equipe': 'Bahrain-McLaren',
		'cout': 15,
	},
	'Wout Van Aert': {
		'equipe': 'Jumbo-Visma',
		'cout': 16,
	}
}
[ele.update(dict(general=None, montagne=None, points=None, jeune=None, etape=0, total=0, rentabilite=0)) for ele in coureurs.values()]


def get_ranking(url,type):
	requete = requests.get(url)
	page = requete.content
	soup = BeautifulSoup(page,features="html.parser")
	table = soup.find_all('figure', attrs={'class':'wp-block-table'})[-1].find('table').find('tbody')

	for line in table.find_all('tr'):
		cols = [ele.text.strip() for ele in line.find_all('td')]
		nom = cols[1].split('(')[0].strip()
		if nom in coureurs: # suppression des abandons
			if type not in 'etape':
				coureurs[nom][type] = cols[0]
			else:
				coureurs[nom][type] += fantasy_etape[type][int(cols[0])-1] if int(cols[0]) <= len(fantasy_etape[type]) else 0
        

def compute_points():
    for coureur, stat in coureurs.items():
        tot = sum([fantasy[key][int(stat[key])-1] if stat[key] and int(stat[key]) <= len(fantasy[key]) else 0 for key in fantasy.keys()])
        coureurs[coureur]["total"] = tot
        coureurs[coureur]["rentabilite"] = round(coureurs[coureur]["total"] / coureurs[coureur]["cout"],1)


def write_csv(file):
	with open(file, 'w', encoding='utf8', newline='') as csvfile:
		fieldnames = ['Coureur', 'Equipe', 'Cout Fantasy', 'Class. Général', 'Class. Montagne', 'Class. Points', 'Class. Jeune','Points Class. Etape','Fantasy Score', 'Rentabilité (Score / Cout)']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		[writer.writerow({
				"Coureur": coureur,
				"Equipe": stat["equipe"],
				"Cout Fantasy": stat["cout"],
				"Class. Général": stat["general"],
				"Class. Montagne": stat["montagne"],
				"Class. Points": stat["points"],
				"Class. Jeune": stat["jeune"],
				"Points Class. Etape": stat["etape"],
				"Fantasy Score": stat["total"],
				"Rentabilité (Score / Cout)": stat["rentabilite"],
		}) for coureur, stat in coureurs.items()]


######
# Main
get_ranking(class_general,"general")
get_ranking(class_montagne,"montagne")
get_ranking(class_points,"points")
get_ranking(class_jeune,"jeune")

for i in range(1,22):
	url = u"https://tourdefrance2020.fr/" + str(i) + "e-etape/"
	get_ranking(url,"etape")

compute_points()
write_csv(file)

# pprint(coureurs)

