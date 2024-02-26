# Créé par gabriel, le 27/03/2023 en Python 3.7
import folium, webbrowser, math, requests, json, csv, urllib.parse
from shapely.geometry import Polygon, Point
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup as bs
from tkinter import *
from math import inf


m = folium.Map(location=[47.472, -0.548], zoom_start=14)



def ouvrircarte():
        html = open('carte.html')
        soup = bs(html, 'html.parser')
        def AddIconTitle():
            new_link = soup.new_tag("link")
            new_title = soup.new_tag("title")
            icon = ('icon.png')
            new_link['rel'] = 'icon'
            new_link['href'] = icon
            new_title.string = "Carte"
            soup.html.head.append(new_link)
            soup.html.head.append(new_title)

        AddIconTitle()
        with open("carte.html", "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))
        webbrowser.open('carte.html')

def minimum(dico):
    mini = inf
    for i in dico.items():
        if type(i)==list:
            for j in i[1]:
                if j[1]<mini:
                    mini = j[1]
                    mini_cle = j[0]
        else:
            if i[1]<mini:
                mini = i[1]
                mini_cle = i[0]
    return mini_cle
def dijkstra(G,s):
    D = {}
    d = {k:inf for k in G}
    parent = {k:None for k in G}
    d[s] = 0
    e = inf
    while e >= 1:
        k = minimum(d)
        for j in range(len(G[k])):
            v,c = G[k][j]
            if v not in D:
                if d[v] > d[k]+c:
                    parent[v] = k
                d[v] = min(d[v],d[k]+c)
        D[k] = d[k]
        del d[k]
        e = 0
        for i in d.keys():
            if d[i] != inf :
                e = e +1
    return D,parent

def solution(end,parents):
    chemin = []
    courant = end
    while courant != None:
        chemin = [courant] + chemin
        courant = parents[courant]
    return chemin

def lieuxprdef():
    tableau = []
    fichier= open("lieuxprdef.csv","r")
    entete = fichier.readline().split(",")
    for ligne in fichier:
        valeurs = ligne.split(",")
        D={}
        for i in range(len(entete)):
            key = entete[i].strip()
            if key == 'x' or key == 'y':
                D[key] = float(valeurs[i])
            else:
                D[key] = valeurs[i]
        tableau.append(D)
    fichier.close()
    return tableau

lieuxprdef = lieuxprdef()
name_lieuxprdef = ["garder lieu personnalisé"]
for i in range(len(lieuxprdef)):
    if lieuxprdef[i]['type']!= "Toilettes Publiques" :
        name_lieuxprdef.append(lieuxprdef[i]['name'])
name_lieuxprdef.append('Toilettes Publiques')
for a in lieuxprdef :
    if a['type'] == 'Toilettes Publiques' :
        folium.Marker(location=[a['x'], a['y']], tooltip=a['type'],
                      icon=folium.Icon(prefix='fa',icon=a['icon'])).add_to(m)
    else:
        folium.Marker(location=[a['x'], a['y']], tooltip=a['name'],
                      icon=folium.Icon(prefix='fa',icon=a['icon'])).add_to(m)





def create():
    win = Toplevel(app)
    win.title('lieuxprdef')
    win.resizable(width=False, height=False)
    win.iconbitmap("icon.ico")
    win.geometry("370x200")

    texte0 = Label(win, text="définire un lieu prédefini :")
    texte0.place(x=15, y=20)
    texte0.config(font=("Arial", 11))

    texte3 = Label(win, text="nom du lieu prédefini :")
    texte3.place(x=10, y=50)
    texte3.config(font=("Arial", 9))
    value_nom_prdef = StringVar()
    entree_nom_prdef = Entry(win, textvariable=value_nom_prdef, width=30)
    entree_nom_prdef.place(x=170, y=50)
    value_nom_prdef.set("")

    texte1 = Label(win, text="numéro du lieu prédefini :")
    texte1.place(x=10, y=80)
    texte1.config(font=("Arial", 9))
    entree_num_prdef = Spinbox(win, from_=0, to=1000)
    entree_num_prdef.place(x=170, y=80)

    texte2 = Label(win, text="nom rue du lieu prédefini :")
    texte2.place(x=10, y=110)
    texte2.config(font=("Arial", 9))
    value_rue_prdef = StringVar()
    entree_rue_prdef = Entry(win, textvariable=value_rue_prdef, width=30)
    entree_rue_prdef.place(x=170, y=110)
    value_rue_prdef.set("")

    rad = Checkbutton(win, text="ajouter ce lieu d'arrivée prédefini", command=lambda: ajouter_lieuxprdef())
    rad.deselect()
    rad.place(x=150, y=150)
    rad.config(font=("Arial", 10))

    def ajouter_lieuxprdef():
            fichiercsv = open('lieuxprdef.csv', 'a', newline='', encoding='utf-8')
            writer = csv.writer(fichiercsv)
            rue_prdef = entree_rue_prdef.get()
            num_prdef = entree_num_prdef.get()
            nom_prdef = entree_nom_prdef.get()
            if rue_prdef != "":
                lieuxprdef_ajouté = str(num_prdef) + ' ' + rue_prdef + ' Angers France'
                endpoint = "https://nominatim.openstreetmap.org/search"
                params_prdef = {
                    "q": lieuxprdef_ajouté,
                    "format": "json",
                    "addressdetails": 1,
                    "limit": 1
                }
                response_prdef = requests.get(endpoint, params=params_prdef).json()
            writer.writerow(['lieu_ajouté', nom_prdef, float(response_prdef[0]["lat"]), float(response_prdef[0]["lon"]),'star'])
            name_lieuxprdef.append(nom_prdef)
            lieu_arriv_pre = name_lieuxprdef
            listeCombo = ttk.Combobox(app, values=lieu_arriv_pre)
            listeCombo.current(0)
            listeCombo.place(x=130, y=295)
            folium.Marker(location=(float(response_prdef[0]["lat"]), float(response_prdef[0]["lon"])), tooltip=nom_prdef,
                          icon=folium.Icon(prefix='fa', icon='star')).add_to(m)



def GetCoords():
    rue_départ = entree_rue_départ.get().lower()
    num_départ = entree_num_départ.get()
    rue_arrivée = entree_rue_arrivé.get().lower()
    num_arrivée = entree_num_arrivé.get()
    if rue_départ == "" or rue_arrivée == "" and listeCombo.get() == "garder lieu personnalisé" :
        labelcalc.config(text=("lieu de départ ou d'arrivée incorrect"))
    if rue_départ != "" and rue_arrivée != "" and listeCombo.get() == "garder lieu personnalisé":
        départ = str(num_départ) + ' ' + rue_départ + ' Angers France'
        arrivée = str(num_arrivée) + ' ' + rue_arrivée + ' Angers France'
        endpoint = "https://nominatim.openstreetmap.org/search"
        params_départ = {
            "q": départ,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_départ = requests.get(endpoint, params=params_départ).json()
        coordonnégpsdépart = (float(response_départ[0]["lat"]), float(response_départ[0]["lon"]))

        params_arrivée = {
            "q": arrivée,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_arrivée = requests.get(endpoint, params=params_arrivée).json()
        coordonnégpsarrivée = (float(response_arrivée[0]["lat"]), float(response_arrivée[0]["lon"]))


    if rue_départ != "" and rue_arrivée == "" and listeCombo.get() != "garder lieu personnalisé" :
        départ = str(num_départ) + ' ' + rue_départ + ' Angers France'
        endpoint = "https://nominatim.openstreetmap.org/search"
        params_départ = {
            "q": départ,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_départ = requests.get(endpoint, params=params_départ).json()
        coordonnégpsdépart = (float(response_départ[0]["lat"]), float(response_départ[0]["lon"]))
        mini = inf
        for i in lieuxprdef :
            if listeCombo.get() == i['name'] :
                coordonnégpsarrivée = (i['x'],i['y'])
            if listeCombo.get() == "Toilettes Publiques" :
                if distanceAB(coordonnégpsdépart, (i['x'], i['y'])) < mini:
                    coordonnégpsarrivée = (i['x'], i['y'])
    if rue_départ != "" and rue_arrivée != "" and listeCombo.get() == "garder lieu personnalisé":
        départ = str(num_départ) + ' ' + rue_départ + ' Angers France'
        arrivée = str(num_arrivée) + ' ' + rue_arrivée + ' Angers France'
        endpoint = "https://nominatim.openstreetmap.org/search"
        params_départ = {
            "q": départ,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_départ = requests.get(endpoint, params=params_départ).json()
        coordonnégpsdépart = (float(response_départ[0]["lat"]), float(response_départ[0]["lon"]))

        params_arrivée = {
            "q": arrivée,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_arrivée = requests.get(endpoint, params=params_arrivée).json()
        coordonnégpsarrivée = (float(response_arrivée[0]["lat"]), float(response_arrivée[0]["lon"]))


    if rue_départ != "" and rue_arrivée == "" and listeCombo.get() != "garder lieu personnalisé" :
        départ = str(num_départ) + ' ' + rue_départ + ' Angers France'
        endpoint = "https://nominatim.openstreetmap.org/search"
        params_départ = {
            "q": départ,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        response_départ = requests.get(endpoint, params=params_départ).json()
        coordonnégpsdépart = (float(response_départ[0]["lat"]), float(response_départ[0]["lon"]))
        mini = inf
        for i in lieuxprdef :
            if listeCombo.get() == i['name'] :
                coordonnégpsarrivée = (i['x'],i['y'])
            if listeCombo.get() == "Toilettes Publiques" :
                if distanceAB(coordonnégpsdépart, (i['x'], i['y'])) < mini:
                    coordonnégpsarrivée = (i['x'], i['y'])
    if rue_départ == "rue de roc epine" :
        folium.PolyLine(chemin_gabriel, tooltip="Chemin", color='purple', opacity='0.6').add_to(m)
        if CheckIfInputInArea(coordonnégpsarrivée) != True:
            labelcalc.config(text=("lieu d'arrivée hors de porté"))
        else:
            folium.Marker(location=[47.48044131026038, -0.5787442235237172], tooltip="Depart", icon=folium.Icon(color='green', prefix='fa', icon='home')).add_to(m)
            return ((47.47628943185663,-0.5662781356294273), coordonnégpsarrivée,1)
    if rue_départ == "rue raoul ponchon" :
        folium.PolyLine(chemin_tom, tooltip="Chemin", color='purple', opacity='0.6').add_to(m)
        if CheckIfInputInArea(coordonnégpsarrivée) != True:
            labelcalc.config(text=("lieu d'arrivée hors de porté"))
        else:
            folium.Marker(location=[47.48854929857258, -0.5658968592137792], tooltip="Depart", icon=folium.Icon(color='green', prefix='fa', icon='home')).add_to(m)
            return ((47.478416612657355,-0.5647017041418715), coordonnégpsarrivée,2)



    if CheckIfInputInArea(coordonnégpsdépart) != True:
        labelcalc.config(text=("lieu de départ hors de porté"))
    elif CheckIfInputInArea(coordonnégpsarrivée) != True:
        labelcalc.config(text=("lieu d'arrivée hors de porté"))
    else:
        return (coordonnégpsdépart, coordonnégpsarrivée,0)



def ptleplusproche(A,inter):
    min = inf
    for i in inter.keys():
        if distanceAB(A,inter[i])<min:
            min = distanceAB(A,inter[i])
            vmin = i
    return vmin
def CheckIfInputInArea(point_coord):
    polygon = Polygon(poly_coords)
    point = Point(reversed(point_coord))
    if polygon.contains(point):
        return True


def temps(a):
    if GetCoords() != None:
        coords = GetCoords()
        if coords[2] == 0 :
            folium.Marker(location=[coords[0][0], coords[0][1]], tooltip="Depart",
                            icon=folium.Icon(color='green', prefix='fa',icon='home')).add_to(m)
        folium.Marker(location=[coords[1][0], coords[1][1]], tooltip="Destination",
                        icon=folium.Icon(color='red', prefix='fa', icon="flag")).add_to(m)
        arrivproche = ptleplusproche(coords[1], E)
        depproche = ptleplusproche(coords[0], E)
        if a==2:
            tableau, parents = dijkstra(D_piéton, depproche)
            path_key = solution(arrivproche, parents)
            path, start, end = GetCoordPath(path_key, coords[0], coords[1])
        else:
            tableau, parents = dijkstra(D, depproche)
            path_key = solution(arrivproche, parents)
            path, start, end = GetCoordPath(path_key, coords[0], coords[1])
        distance_mètre = calculate_path_distance(path_key)


        if coords[2] == 1:
            distance_mètre = calculate_path_distance(path_key) + 2000
        if coords[2] == 2:
            distance_mètre = calculate_path_distance(path_key) + 1400
        if a==2:
            temps = ((distance_mètre / 1000 / 5.2) * 60 * 60)
            if temps // 360 == 0:
                heure = 0
                minute = int(temps // 60)
                seconde = int(temps % 60)
            else:
                heure = int(temps // 3600)
                minute = int((temps - heure * 3600) // 60)
                seconde = int((temps - heure * 3600) % 60)
        if a==1:
            temps = ((distance_mètre / 1000 / 15) * 60 * 60)
            if temps // 360 == 0:
                heure = 0
                minute = int(temps // 60)
                seconde = int(temps % 60)
            else:
                heure = int(temps // 3600)
                minute = int((temps - heure * 3600) // 60)
                seconde = int((temps - heure * 3600) % 60)
        if a==3:
            temps = ((distance_mètre / 1000 / 30) * 60 * 60)
            if temps // 360 == 0:
                heure = 0
                minute = int(temps // 60)
                seconde = int(temps % 60)
            else:
                heure = int(temps // 3600)
                minute = int((temps - heure * 3600) // 60)
                seconde = int((temps - heure * 3600) % 60)
        labelcalc.config(text=(heure,"h",minute,"min",seconde,"s", "/", distance_mètre, "m"))
        folium.PolyLine(path, tooltip="Chemin", color='blue', opacity='0.6').add_to(m)
        folium.PolyLine(start, tooltip="Chemin", color='red', dash_array=[5, 5], opacity='0.5').add_to(m)
        folium.PolyLine(end, tooltip="Chemin", color='red', dash_array=[5, 5], opacity='0.5').add_to(m)
        m.save("carte.html")



app = Tk()
app.title("calcule itinéraire le plus court")
app.resizable(width=False, height=False)
app.iconbitmap("icon.ico")

C = Canvas(app, bg="blue", height=450, width=600)
filename = PhotoImage(file="fond.png")
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

texte = Label(app, text="Calculer l'itinéraire le plus court :")
texte.place(x=190, y=53)
texte.config(bg="#B8DBF7", font=("Arial", 12))

texte0 = Label(app, text="lieu de départ :")
texte0.place(x=140, y=83)
texte0.config(bg="#B8DBF7", font=("Arial", 11))

texte1 = Label(app, text="numéro de départ :")
texte1.place(x=125, y=110)
texte1.config(bg="#B8DBF7", font=("Arial", 9))
entree_num_départ = Spinbox(app, from_=0, to=1000)
entree_num_départ.place(x=240, y=110)

texte2 = Label(app, text="nom rue de départ :")
texte2.place(x=125, y=130)
texte2.config(bg="#B8DBF7", font=("Arial", 9))
value_rue_départ = StringVar()
entree_rue_départ = Entry(app, textvariable=value_rue_départ, width=30)
entree_rue_départ.place(x=240, y=130)
value_rue_départ.set("")

texte4 = Label(app, text="lieu d'arrivée :")
texte4.place(x=140, y=175)
texte4.config(bg="#B8DBF7", font=("Arial", 11))

texte5 = Label(app, text="numéro d'arrivée :")
texte5.place(x=125, y=202)
texte5.config(bg="#B8DBF7", font=("Arial", 9))
entree_num_arrivé = Spinbox(app, from_=0, to=1000)
entree_num_arrivé.place(x=240, y=202)

texte6 = Label(app, text="nom rue d'arrivée :")
texte6.place(x=125, y=222)
texte6.config(bg="#B8DBF7", font=("Arial", 9))
value_rue_arrivé = StringVar()
entree_rue_arrivé = Entry(app, textvariable=value_rue_arrivé, width=30)
entree_rue_arrivé.place(x=240, y=222)
value_rue_arrivé.set("")

texte8 = Label(app, text="choisir un lieu d'arrivée prédefini :")
texte8.place(x=125, y=265)
texte8.config(bg="#B8DBF7", font=("Arial", 11))
lieu_arriv_pre = name_lieuxprdef
listeCombo = ttk.Combobox(app, values=lieu_arriv_pre, state= 'readonly',height=8)
listeCombo.current(0)
listeCombo.place(x=130, y=295)

rad5 = Checkbutton(app, text="ajouter un lieu d'arrivée prédefini" , command =lambda: create())
rad5.deselect()
rad5.place(x=280, y=292)
rad5.config(bg="#B8DBF7", font=("Arial", 10))



texte9 = Label(app, text="choisir un moyen de transport :")
texte9.place(x=125, y=320)
texte9.config(bg="#B8DBF7", font=("Arial", 11))

radiovalue = IntVar()

rad1 = Checkbutton(app, text='voiture',variable=radiovalue, onvalue=3,command=lambda: temps(3))
rad1.deselect()
rad1.place(x=125, y=355)
rad1.config(bg="#B8DBF7", font=("Arial", 9))
rad2 = Checkbutton(app, text='vélo',variable=radiovalue, onvalue=1,command=lambda: temps(1))
rad2.deselect()
rad2.place(x=190, y=355)
rad2.config(bg="#B8DBF7", font=("Arial", 9))
rad3 = Checkbutton(app, text='à pied', variable=radiovalue, onvalue=2,command=lambda: temps(2))
rad3.deselect()
rad3.place(x=240, y=355)
rad3.config(bg="#B8DBF7", font=("Arial", 9))

labelcalc = Label(app, text="temps nécessaire/distance")
labelcalc.config(bg="white", font=("Arial", 10))
labelcalc.place(x=320, y=356)

boutoncarte = Checkbutton(app, text="générer la carte", command=lambda: ouvrircarte())
boutoncarte.place(x=320, y=386)
boutoncarte.config(bg="white")


def distanceAB(A, B):
    a = math.sin(A[0] * math.pi / 180)
    b = math.sin(B[0] * math.pi / 180)
    c = math.cos(A[0] * math.pi / 180)
    d = math.cos(B[0] * math.pi / 180)
    e = math.cos((B[1] * math.pi / 180) - (A[1] * math.pi / 180))
    distance = round((60 * math.acos(a * b + c * d * e) * 180 / math.pi), 3)
    distance_mètre = round((distance * 1.852 * 1000), 0)
    return distance_mètre




def calculate_path_distance(path):
    distance = 0
    for i in range(len(path) - 1):
        node1 = E[path[i]]
        node2 = E[path[i + 1]]
        distance += distanceAB(node1, node2)
    return round(distance, None)


def GetCoordPath(path, start, end):
    main_path = []
    start_path = []
    end_path = []

    for i in range(len(path)):
        main_path.append(E[path[i]])
    start_path.append(start)
    start_path.append(main_path[0])
    end_path.append(end)
    end_path.append(main_path[-1])


    return (main_path, start_path, end_path)


def extract_coords():
    with open('inter_angers.geojson', 'r') as f:
        geojson_data = json.load(f)

    E = {}
    for feature in geojson_data['features']:
        name = feature['properties']['name']
        lat, lon = feature['geometry']['coordinates']
        key = 'S{}'.format(name[3:])
        E[key] = (lon, lat)

    return E


E = extract_coords()


def create_dict_dijkstra():
    with open('dijkstra.csv', 'r') as f:
        dijkstra = csv.reader(f, delimiter=';')
        D = {}

        for row in dijkstra:
            all_columns = []
            for i in range(1, len(row)):
                all_columns.append((row[i], distanceAB(E[row[0]], E[row[i]])))
            D[str(row[0])] = (all_columns)

        return D

def create_dict_dijkstra_piéton():
    with open('dijkstra_piéton.csv', 'r') as f:
        dijkstra = csv.reader(f, delimiter=';')
        D = {}
        for row in dijkstra:
            all_columns = []
            for i in range(1, len(row)):
                all_columns.append((row[i], distanceAB(E[row[0]], E[row[i]])))
            D[str(row[0])] = (all_columns)

        return D



D = create_dict_dijkstra()
D_piéton = create_dict_dijkstra_piéton()


poly_coords = [(-0.5645295178630684, 47.470930454186316), (-0.5625491299818349, 47.47016476920214),
               (-0.5617839801186312, 47.469890945374004), (-0.5586216843662378, 47.46860026465998),
               (-0.5555779133177977, 47.46747020246033),
               (-0.5512718145801863, 47.467971436068865), (-0.5499535479554677, 47.46996464326821),
               (-0.5492113459078386, 47.469482226417625), (-0.548112722524244, 47.470307974744344),
               (-0.5471808724160994, 47.47140912166938),
               (-0.5465928200245164, 47.47213464833348), (-0.5463447193717225, 47.47311530979721),
               (-0.5463263347347271, 47.47340112632898), (-0.5485692604481628, 47.47438697432173),
               (-0.5492463758859314, 47.475333395230365),
               (-0.5503310694686586, 47.47585529786858), (-0.5514689605535434, 47.476589193159754),
               (-0.5536262232631113, 47.47749089291099), (-0.5554272872657827, 47.47823920118884),
               (-0.5562028162414371, 47.47860817876685),
               (-0.5577219045717021, 47.47910630581984), (-0.5582423253316806, 47.479226997713425),
               (-0.5605077250761608, 47.47914766604873), (-0.5634312652278058, 47.479040767366996),
               (-0.5647017041418715, 47.478416612657355),
               (-0.5657588212710473, 47.47737167721985), (-0.5662781356294273, 47.47628943185663),
               (-0.5670747247904943, 47.4748941463626), (-0.5670507282676894, 47.47427477626994),
               (-0.5663822330651195, 47.473170242295225),
               (-0.5645295178630684, 47.470930454186316)]
chemin_gabriel = [(47.48042630991767,-0.5787346152966832),(47.47985465984408,-0.5780488580795318),(47.479543214858495,-0.5771031759872969),(47.481937913746826,-0.577176108387556),(47.481369121658425,-0.5742169282627363),(47.4776607990942,-0.5682421468069099),(47.47689148243042,-0.567455375049446),(47.47628943185663,-0.5662781356294273)]
chemin_tom = [(47.48854929857258,-0.5658968592137792),(47.487320906469556,-0.5660068503859494),(47.48714925971245,-0.5653078666557132),(47.48695471406947,-0.5643201515951524),(47.48661670404318,-0.5634638903423705),(47.48075008016426,-0.5642277166454379),(47.480218093593486,-0.5645089834877148),(47.4799152269116,-0.5644270376233407),(47.47878920052157,-0.565031512816141),(47.478416612657355,-0.5647017041418715)]
C.pack()
app.mainloop()