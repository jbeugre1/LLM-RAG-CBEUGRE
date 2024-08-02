import igraph as ig
import gravis as gv


def get_direction(start_room ,end_room):
    # Création du graphe
    graph = ig.Graph(directed=False)

    # Dictionnaire pour mapper les noms de salles aux indices
    room_indices = {}
    current_index = 0

    # Fonction pour ajouter des salles et connexions
    def add_level_connections(level_name, rooms, graph, room_indices, current_index):
        previous_room = None
        first_room = None
        for room in rooms:
            if room not in room_indices:
                room_indices[room] = current_index
                graph.add_vertex(name=room)
                current_index += 1
            
            if previous_room is not None:
                graph.add_edge(room_indices[previous_room], room_indices[room], type='simple_path')
            else:
                first_room = room
            
            previous_room = room

        # Connect the last room back to the first to form a circular connection
        graph.add_edge(room_indices[previous_room], room_indices[first_room], type='simple_path')

        return current_index

    # Ajout des salles et connexions pour chaque niveau
    levels = {
        'RDJ': ['EP', 'Auditorium', 'Comoe', 'Bandama', 'Ascenseur BRDJ', 'Kouroukoule', 'Cavally', 'Ascenseur CRDJ', 'Restaurant', 'Ascenseur DRDJ', 'Salle_de_sport', 'sans_pedro', 'Alepe', 'Soubre', 'Ascenseur ARDJ', 'EP'],
        '0': ['Acceuil', 'Ascenseur B0', 'Kossou', 'Buyo', 'Niari', 'Ascenseur C0', 'Toumodi', 'goal24', 'Ascenseur D0', 'Bongouanou', 'Dimbokro', 'Tiassale', 'Ascenseur A0', 'Acceuil'],
        '1': ['Ganoa', 'Ascenseur B1', 'Daloa', 'Vavoua', 'Ascenseur C1', 'Bondoukou', 'Man', 'Ascenseur D1', 'Bouake', 'Danane', 'Zuenola', 'Ascenseur A1', 'Yamoussoukro', 'Ganoa'],
        '2': ['Katiola', 'Ascenseur B2', 'Tanda', 'Mankono', 'Ascenseur C2', 'Kani', 'Seguela', 'Ascenseur D2', 'Bassawa', 'Nassian', 'Bouna', 'Ascenseur A2', 'Worofla', 'Katiola'],
        '3': ['Ascenseur B3', 'Gan', 'Bako', 'Ascenseur C3', 'Noungang', 'Borotou', 'Ascenseur D3', 'Kanakono', 'Tienko', 'Minignan', 'Ascenseur A3', 'Espace_repo', 'Ascenseur B3'],
        '4': ['Espace_repo1', 'PCA', 'Ascenseur B4', 'Ascenseur C4', 'Korhogo', 'Boundiali', 'Ascenseur D4', 'salle', 'Niélé', 'Espace_repo2'],
        '5': ['Espace_repo1', 'Teheni', 'Ascenseur B5', 'Tengrela', 'Ascenseur D5', 'Kouto', 'Espace_repo2']
    }

    for level, rooms in levels.items():
        current_index = add_level_connections(level, rooms, graph, room_indices, current_index)

    # Ajout des connexions verticales (ascenseurs)
    vertical_connections = [
        ('Ascenseur CRDJ', 'Ascenseur C0', 'Ascenseur C1', 'Ascenseur C2', 'Ascenseur C3', 'Ascenseur C4'),
        ('Ascenseur BRDJ', 'Ascenseur B0', 'Ascenseur B1', 'Ascenseur B2', 'Ascenseur B3', 'Ascenseur B4', 'Ascenseur B5'),
        ('Ascenseur DRDJ', 'Ascenseur D0', 'Ascenseur D1', 'Ascenseur D2', 'Ascenseur D3', 'Ascenseur D4', 'Ascenseur D5'),
        ('Ascenseur ARDJ', 'Ascenseur A0', 'Ascenseur A1', 'Ascenseur A2', 'Ascenseur A3')
    ]

    for vertical_set in vertical_connections:
        for i in range(len(vertical_set) - 1):
            graph.add_edge(room_indices[vertical_set[i]], room_indices[vertical_set[i + 1]], type='elevator')


    
    shortest_path = graph.get_shortest_paths(room_indices[start_room], to=room_indices[end_room], output='vpath')

    # Affichage du chemin le plus court
    shortest_path_rooms = [graph.vs[vertex]['name'] for vertex in shortest_path[0]]
    #print(f"Le chemin le plus court entre {start_room} et {end_room} est :")
    #print(" -> ".join(shortest_path_rooms))
    
    shortest = " -> ".join(shortest_path_rooms)
    
    return shortest
    
    
    


    