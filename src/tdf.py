import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv
from data2023 import coureurs

file = 'ranking.csv'

website = u"https://tourdefrance2023.fr"
class_general = f"{website}/classement-general/"
class_montagne = f"{website}/classement-du-meilleur-grimpeur/"
class_points = f"{website}/classement-par-points/"
class_jeune = f"{website}/classement-du-meilleur-jeune/"

fantasy = {
    "general": [50, 45, 40, 35, 30, 28, 26, 24, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10,10,10,10,10, 9,9,9,9,9, 8,8,8,8,8, 7,7,7,7,7, 6,6,6,6,6, 5,5,5,5,5, 4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3,3,3,3,3, 2,2,2,2,2,2,2,2,2,2, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    "montagne": [30, 26, 22, 20, 18, 16, 14 ,12, 10, 8, 6, 4, 3, 2, 1],
    "points": [30, 26, 22, 20, 18, 16, 14 ,12, 10, 8, 6, 4, 3, 2, 1],
    "jeune": [20, 18, 16, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
	"etape": [200, 150, 120, 100, 90, 80, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 9, 8,8,8,8,8, 7,7,7,7,7, 6,6,6,6,6, 5,5,5,5,5, 4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3,3,3,3,3, 2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
}


def get_ranking(url,type,index):
	print(url)
	requete = requests.get(url)
	page = requete.content
	soup = BeautifulSoup(page,features="html.parser")
	table = soup.find_all('figure', attrs={'class':'wp-block-table'})[index].find('table').find('tbody')

	for line in table.find_all('tr'):
		cols = [ele.text.strip() for ele in line.find_all('td')]
		nom = cols[1].split('(')[0].strip()
		if nom in coureurs: # suppression des abandons
			if type not in 'etape':
				coureurs[nom][type] = cols[0]
			else:
				coureurs[nom]["etape"] += fantasy["etape"][int(cols[0])-1] if int(cols[0]) <= len(fantasy["etape"]) else 0

def compute_points():
    for coureur, stat in coureurs.items():
        tot = sum([fantasy[key][int(stat[key])-1] if stat[key] and int(stat[key]) <= len(fantasy[key]) else 0 for key in ("general","montagne","points","jeune")])
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
get_ranking(class_general,"general", 0)
get_ranking(class_montagne,"montagne", 0)
get_ranking(class_points,"points", 0)
get_ranking(class_jeune,"jeune", 0)

for i in range(1,22):
	url = f"{website}/etape-{i}/"
	get_ranking(url,"etape", -1)

compute_points()
write_csv(file)

pprint(coureurs)

