import igraph as ig

# Création du graphe
graph = ig.Graph(directed=False)

# Dictionnaire pour mapper les noms de salles aux indices
room_indices = {}
current_index = 0

# Fonction pour ajouter des salles et connexions avec directions
def add_level_connections(level_name, rooms, directions, graph, room_indices, current_index):
        previous_room = None
        first_room = None
        for i, room in enumerate(rooms):
            if room not in room_indices:
                room_indices[room] = current_index
                graph.add_vertex(name=room)
                current_index += 1
            
            if previous_room is not None:
                direction = directions.get((previous_room, room), "unknown")
                graph.add_edge(room_indices[previous_room], room_indices[room], type='simple_path', direction=direction)
            else:
                first_room = room
            
            previous_room = room

        # Connect the last room back to the first to form a circular connection
        direction = directions.get((previous_room, first_room), "unknown")
        graph.add_edge(room_indices[previous_room], room_indices[first_room], type='simple_path', direction=direction)

        return current_index

# Directions for each pair of rooms (example directions, you should adjust as needed)
level_directions = {
    
    'RDJ': {
        ('Cavally','Kouroukelé'):'gauche',
        ('Kouroukelé','Sassandra'):'gauche',('Kouroukelé','Cavally'):'droite',
        ('Sassandra','Kouroukelé'):'droite',('Sassandra','Ascenseur_BRDJ'):'juste en face',
        ('Ascenseur_BRDJ','Sassandra'):'juste en face',('Ascenseur_BRDJ','Bandama'):'gauche puis droite',
        ('Bandama','Comoe'):'gauche',('Bandama','Ascenseur_BRDJ'):'depasser la salle bandama puis droite',
        ('Comoe','Bandama'):"gauche",('Comoe','Entree_Principal'):'aller tout droit puis a droite passer la porte et prendre l\'autre porte a droite',
        ('Entree_Principal','Comoe'):"premiere porte a gauche puis a droite et au bout",('Entree_Principal','Soubre'): "prendre la porte a droite et tout droit",
        ('Soubre','Assini'):"droite",('Soubre','Entree_Principal'):"gauche",
        ('Assini','Soubre'):'juste en face',('Assini','Ascenseur_ARDJ'):'gauche puis gauche',
        ('Ascenseur_ARDJ','Assini'):'droite puis droite',('Ascenseur_ARDJ','Adiaké'):'droite puis gauche',
        ('Adiaké','Ascenseur_ARDJ'):'droite puis droite',('Adiaké','Aboisso'):'gauche',
        ('Aboisso','Adiaké'):"droite",('Aboisso','Bassam'):"gauche",
        ('Bassam','Aboisso'):"droite",('Bassam','Ayame'):"gauche",
        ('Ayame','Bassam'):"droite",('Ayame','San_Pedro'):"en face",
        ('San_Pedro','Ayame'):'en face',('San_Pedro','Alepe'):'en face',
        ('Alepe','San_Pedro'):'en face',('Alepe','Ascenseur_CRDJ'):'prendre la porte a gauche puis a droite. Tout droit puis a droite',
        ('Ascenseur_CRDJ','Alepe'):'droite puis gauche. Gauche puis droite',('Ascenseur_CRDJ','Restaurant'):'droite puis droite',
        ('Restaurant','Ascenseur_CRDJ'):'gauche en faisant face au centre du batiment puis a gauche',('Restaurant','Ascenseur_DRDJ'):"droite en faisant face au centre du batiment puis droite",
        ('Ascenseur_DRDJ','Restaurant'):'gauche puis gauche',('Ascenseur_DRDJ','Ascenseur_BRDJ'):"gauche puis droite. puis droite puis gauche. Tout droite puis a droite a la premiere porte",
        ('Ascenseur_BRDJ','Ascenseur_DRDJ'):'gauche puis gauche'
    },
    '0': {
        ('Acceuil','Ascenseur_B0'):'gauche puis gauche',('Acceuil','Ascenseur_A0'):'droite puis droite',
        ('Ascenseur_B0','Acceuil'):'droite puis droite',('Ascenseur_B0','Kossou'):"gauche puis droite",
        ('Kossou','Ascenseur_B0'):'gauche puis gauche',('Kossou','Buyo'):'droite',
        ('Buyo','Kossou'):'gauche',('Buyo','Niari'):'droite',
        ('Niari','Buyo'):'gauche',('Niari','Ascenseur_C0'):'droite puis droite',
        ('Ascenseur_C0','Niari'):'droite puis gauche',('Ascenseur_C0','Toumodi'):'gauche puis gauche',
        ('Toumodi','Ascenseur_C0'):'gauche puis droite',('Toumodi','goal24'):'droite',
        ('goal24','Toumodi'):'gauche',('goal24','Ascenseur_D0'):'droite puis gauche',
        ('Ascenseur_D0','goal24'):'droite puis droite',('Ascenseur_D0','Bongouanou'):'droite puis gauche',
        ('Bongouanou','Ascenseur_D0'):'gauche puis droite',('Bongouanou','Dimbokro'):'droite',
        ('Dimbokro','Bongouanou'):'gauche',('Dimbokro','Tiassale'):'droite',
        ('Tiassale','Dimbokro'):'gauche',('Tiassale','Ascenseur_A0'):'droite puis gauche',
        ('Ascenseur_A0','Tiassale'):'gauche puis droite',('Ascenseur_A0','Acceuil'):'gauche puis gauche'

    },
    '1': {
        ('Gagnoa', 'Ascenseur_B1'):'droite puis a gauche' , ('Gagnoa', 'Yamoussoukro'): 'gauche, traversé le pont puis rentré dans le bureau de la dxc',
        ('Ascenseur_B1', 'Daloa'): 'droite puis gauche',('Ascenseur_B1', 'Gagnoa'): 'droite puis droite',
        ('Daloa','Ascenseur_B1'): 'gauche puis droite',('Daloa','Vavoua'):'droite',
        ('Vavoua','Daloa'):'gauche',('Vavoua','Ascenseur_C1'):'droite',
        ('Ascenseur_C1','Vavoua'):'gauche ensuite droite, traversé le bureaux',('Ascenseur_C1','Bondoukou'):'gauche puis gauche',
        ('Bondoukou','Ascenseur_C1'):'gauche puis droite',('Bondoukou','Man'):'droite',
        ('Man','Bondoukou'):'gauche',('Man','Ascenseur_D1'):'droite puis gauche',
        ('Ascenseur_D1','Man'):'droite puis droite ',('Ascenseur_D1','Bouake'):'droite puis gauche',
        ('Bouake','Ascenseur_D1'):'gauche puis droite',('Bouake','Danane'):'droite',
        ('Danane','Bouake'):'gauche',('Danane','Zuenola'):'droite',
        ('Zuenola','Danane'):'gauche',('Zuenola','Ascenseur_A1'):'droite puis gauche',
        ('Ascenseur_A1','Zuenola'):'gauche puis droite',('Ascenseur_A1','Yamoussoukro'):'gauche puis gauche',
        ('Yamoussoukro','Ascenseur_A1'):'sortir du bureau de la DXC à gauche puis a droite ',('Yamoussoukro','Gagnoa'):'droite traversé le bureau de la dxc puis le pont entré dans l\'autre bureau de la dxc'
        
    },
    '2': {
        ('Katiola','Ascenseur_B2'):'droite puis gauche',('Katiola','Worofla'):'gauche puis traverser le pont',
        ('Ascenseur_B2','Katiola'):'droite puis droite',('Ascenseur_B2','Tanda'):'droite puis gauche',
        ('Tanda','Ascenseur_B2'):'gauche puis droite',('Tanda','Mankono'):'droite',
        ('Mankono','Ascenseur_C2'):'droite puis a gauche',('Mankono','Tanda'):'gauche',
        ('Ascenseur_C2','Mankono'):'gauche puis droite',('Ascenseur_C2','Kani'):'gauche puis gauche',
        ('Kani','Ascenseur_C2'):'gauche puis droite',('Kani','Seguela'):'droite',
        ('Seguela','Kani'):'droite',('Seguela','Ascenseur_D2'):'droite puis gauche',
        ('Ascenseur_D2','Seguela'):'droite puis droite',('Ascenseur_D2','Bassawa'):'droite puis gauche',
        ('Bassawa','Ascenseur_D2'):'gauche puis droite ',('Bassawa','Nassian'):'droite',
        ('Nassian','Bassawa'):'gauche',('Nassian','Bouna'):'droite',
        ('Bouna','Nassian'):'gauche',('Bouna','Ascenseur_A2'):'droite puis gauche',
        ('Ascenseur_A2','Bouna'):'gauche puis droite',('Ascenseur_A2','Worofla'):'gauche puis gauche',
        ('Worofla','Ascenseur_A2'):"gauche puis droite",('Worofla','Katiola'):'droite puis traverser le pont'
   
    },
    '3': {
        ('Espace_repo3','Ascenseur_B3'):'rentrez dans le batiment a gauche lorsque vous faites face au centre du batiment puis a gauche',('Espace_repo3','Ascenseur_A3'):'rentrez dans le batiment a droite lorsque vous faites face au centre du batiment puis a droite',
        ('Ascenseur_B3','Espace_repo3'):'droite puis droite',('Ascenseur_B3','Gan'):'droite puis gauche',
        ('Gan','Ascenseur_B3'):'gauche puis droite',('Gan','Bako'):'droite',
        ('Bako','Gan'):'gauche',('Bako','Ascenseur_C3'):'droite puis a gauche',
        ('Ascenseur_C3','Bako'):'gauche puis droite',('Ascenseur_C3','Borotou'):'gauche puis gauche',
        ('Borotou','Ascenseur_C3'):'droite puis droite',('Borotou','Touba'):'droite',
        ('Touba','Borotou'):'gauche',('Touba','Ascenseur_D3'):'droite puis gauche',
        ('Ascenseur_D3','Borotou'):'droite puis droite',('Ascenseur_D3','Kanakono'):'droite puis gauche',
        ('Kanakono','Ascenseur_D3'):'gauche puis droite',('Kanakono','Tienko'):'juste à gauche',
        ('Tienko','Kanakono'):'juste à droite',('Tienko','Odienné'):'sors du batiment a droite',
        ('Odienné','Tienko'):"gauche puis droite",('Odienné','Minignan'):"droite",
        ('Minignan','Odienné'):"gauche",('Minignan','Ascenseur_A3'):"droite puis gauche",
        ('Ascenseur_A3','Minignan'):"gauche",('Ascenseur_A3','Espace_repo3'):'gauche puis gauche'
    },
    '4': {
        ('Espace_repo4_1','PCA'):'rentré dans le batiment',
        ('PCA','Espace_repo4_1'):'gauche',('PCA','Ascenseur_C4'):'droite puis gauche',
        ('Ascenseur_C4','PCA'):'gauche puis droite',('Ascenseur_C4','Korhogo'):"gauche puis gauche",
        ('Korhogo','Ascenseur_C4'):'gauche puis droite',('Korhogo','Boundiali'):'droite',
        ('Boundiali','Korhogo'):'gauche',('Boundiali','Ascenseur_D4'):'droite puis gauche',
        ('Ascenseur_D4','Niélé'):'droite puis puis droite',('Ascenseur_C4','Korhogo'):'droite puis gauche',
        ('Ascenseur_D4','Boundiali'):'droite puis droite',('Ascenseur_D4','Niélé'):'droite puis gauche',
        ('Niélé','Ascenseur_D4'):'gauche puis droite',('Niélé','Espace_repo4_2'):"gauche",
        ('Espace_repo4_2','Niélé'):'rentré dans le batiment'
        
    },
    '5': {
        ('Espace_repo5_1','Teheni'):'rentré dans le batiment puis dans la salle juste devant l\'entré',
        ('Teheni','Espace_repo1'):'gauche',('Teheni','Ascenseur_C5'):'droite puis gauche',
        ('Ascenseur_C5','Teheni'):'gauche puis droite',('Ascenseur_C5','Tengrela'):'droite puis gauche',
        ('Tengrela','Ascenseur_C5'):'droite jusqu\'a la porte puis a droite',('Tengrela','Ascenseur_D5'):'sortez de la piece, puis a droite depasser l\'ascenseur puis tournez a gauche, traversé la salle du milieu puis tourné a gauche apres la porte',
        ('Ascenseur_D5','Tengrela'):'droite puis a droite, traversé la salle du milieu et tourné au niveau de l\'ascenseur a droite, finalement rentré dans la piece a gauche',('Ascenseur_D5','Kouto'):'droite puis gauche',
        ('Kouto','Ascenseur_D5'):'gauche puis droite',('Kouto','Espace_repo5_2'):'gauche',
        ('Espace_repo5_2','Kouto'):'rentré dans le batiment'
    }
}

# Ajout des salles et connexions pour chaque niveau
levels = {
    'RDJ': ['Cavally','Kouroukelé','Sassandra','Ascenseur_BRDJ','Bandama','Comoe','Entree_Principal','Soubre','Assini','Ascenseur_ARDJ','Adiaké','Aboisso','Bassam','Ayame','San_Pedro','Alepe','Ascenseur_CRDJ','Restaurant','Ascenseur_DRDJ','Ascenseur_BRDJ'],
    '0': ['Acceuil', 'Ascenseur_B0', 'Kossou', 'Buyo', 'Niari', 'Ascenseur_C0', 'Toumodi', 'goal24', 'Ascenseur_D0', 'Bongouanou', 'Dimbokro', 'Tiassale', 'Ascenseur_A0', 'Acceuil'],
    '1': ['Gagnoa', 'Ascenseur_B1', 'Daloa', 'Vavoua', 'Ascenseur_C1', 'Bondoukou', 'Man', 'Ascenseur_D1', 'Bouake', 'Danane', 'Zuenola', 'Ascenseur_A1', 'Yamoussoukro', 'Gagnoa'],
    '2': ['Katiola', 'Ascenseur_B2', 'Tanda', 'Mankono', 'Ascenseur_C2', 'Kani', 'Seguela', 'Ascenseur_D2', 'Bassawa', 'Nassian', 'Bouna', 'Ascenseur_A2', 'Worofla', 'Katiola'],
    '3': ['Espace_repo3','Ascenseur_B3', 'Gan', 'Bako', 'Ascenseur_C3', 'Borotou', 'Touba', 'Ascenseur_D3', 'Kanakono', 'Tienko','Odienné', 'Minignan', 'Ascenseur_A3','Espace_repo3'],
    '4': ['Espace_repo4_1', 'PCA', 'Ascenseur_C4', 'Korhogo','Boundiali', 'Ascenseur_D4', 'Niélé', 'Espace_repo4_2'],
    '5': ['Espace_repo5_1', 'Teheni', 'Ascenseur_C5', 'Tengrela', 'Ascenseur_D5', 'Kouto', 'Espace_repo5_2']
}

for level, rooms in levels.items():
    directions = level_directions[level]
    current_index = add_level_connections(level, rooms, directions, graph, room_indices, current_index)

# Ajout des connexions verticales (ascenseurs) avec directions
vertical_connections = [
    ('Ascenseur_CRDJ', 'Ascenseur_C0', 'Ascenseur_C1', 'Ascenseur_C2', 'Ascenseur_C3', 'Ascenseur_C4','Ascenseur_C5'),
    ('Ascenseur_BRDJ', 'Ascenseur_B0', 'Ascenseur_B1', 'Ascenseur_B2', 'Ascenseur_B3'), 
    ('Ascenseur_DRDJ', 'Ascenseur_D0', 'Ascenseur_D1', 'Ascenseur_D2', 'Ascenseur_D3', 'Ascenseur_D4', 'Ascenseur_D5'),
    ('Ascenseur_ARDJ', 'Ascenseur_A0', 'Ascenseur_A1', 'Ascenseur_A2', 'Ascenseur_A3')
]

vertical_directions = [
    ['up', 'up', 'up', 'up', 'up', 'up'],
    ['up', 'up', 'up', 'up'],
    ['up', 'up', 'up', 'up', 'up', 'up'],
    ['up', 'up', 'up', 'up']
]

for vertical_set, directions in zip(vertical_connections, vertical_directions):
    for i in range(min(len(vertical_set) - 1, len(directions))):
        if vertical_set[i] in room_indices and vertical_set[i + 1] in room_indices:
            graph.add_edge(room_indices[vertical_set[i]], room_indices[vertical_set[i + 1]], type='elevator', direction=directions[i])
        else:
            print(f"Missing room: {vertical_set[i]} or {vertical_set[i + 1]}")

start_room = 'Comoe'
end_room = 'Assini'
shortest_path = graph.get_shortest_paths(room_indices[start_room], to=room_indices[end_room], output='vpath')

# Affichage du chemin le plus court avec directions
print(f"Le chemin le plus court entre {start_room} et {end_room} est :")

for i in range(len(shortest_path[0]) - 1):
    src_index = shortest_path[0][i]
    tgt_index = shortest_path[0][i + 1]
    src = graph.vs[src_index]['name']
    tgt = graph.vs[tgt_index]['name']
    edge = graph.es.find(_source=src_index, _target=tgt_index)
    direction = edge['direction']
    print(f"{src} -> {direction} -> {tgt}")
    
