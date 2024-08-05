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
        'RDJ': ['Entree principal', 'Auditorium', 'Comoe', 'Bandama', 'Ascenseur B_RDJ', 'Kouroukoule', 'Cavally', 'Ascenseur C_RDJ', 'Restaurant', 'Ascenseur D_RDJ', 'Salle_de_sport', 'sans_pedro', 'Alepe', 'Soubre', 'Ascenseur A_RDJ', 'EP'],
        '0': ['Acceuil', 'Ascenseur B_0', 'Kossou', 'Buyo', 'Niari', 'Ascenseur C_0', 'Toumodi', 'goal24', 'Ascenseur D_0', 'Bongouanou', 'Dimbokro', 'Tiassale', 'Ascenseur A_0', 'Acceuil'],
        '1': ['Ganoa', 'Ascenseur B_1', 'Daloa', 'Vavoua', 'Ascenseur C_1', 'Bondoukou', 'Man', 'Ascenseur D_1', 'Bouake', 'Danane', 'Zuenola', 'Ascenseur A_1', 'Yamoussoukro', 'Ganoa'],
        '2': ['Katiola', 'Ascenseur B_2', 'Tanda', 'Mankono', 'Ascenseur C_2', 'Kani', 'Seguela', 'Ascenseur D_2', 'Bassawa', 'Nassian', 'Bouna', 'Ascenseur A_2', 'Worofla', 'Katiola'],
        '3': ['Ascenseur B_3', 'Gan', 'Bako', 'Ascenseur C_3', 'Noungang', 'Borotou', 'Ascenseur D_3', 'Kanakono', 'Tienko', 'Minignan', 'Ascenseur A_3', 'Espace_repo', 'Ascenseur B_3'],
        '4': ['Espace_repo1', 'PCA', 'Ascenseur B_4', 'Ascenseur C_4', 'Korhogo', 'Boundiali', 'Ascenseur D_4', 'salle', 'Niélé', 'Espace_repo2'],
        '5': ['Espace_repo1', 'Teheni', 'Ascenseur B_5', 'Tengrela', 'Ascenseur D_5', 'Kouto', 'Espace_repo2']
    }

    for level, rooms in levels.items():
        current_index = add_level_connections(level, rooms, graph, room_indices, current_index)

    # Ajout des connexions verticales (ascenseurs)
    vertical_connections = [
        ('Ascenseur C_RDJ', 'Ascenseur C_0', 'Ascenseur C_1', 'Ascenseur C_2', 'Ascenseur C_3', 'Ascenseur C_4'),
        ('Ascenseur B_RDJ', 'Ascenseur B_0', 'Ascenseur B_1', 'Ascenseur B_2', 'Ascenseur B_3', 'Ascenseur B_4', 'Ascenseur B_5'),
        ('Ascenseur D_RDJ', 'Ascenseur D_0', 'Ascenseur D_1', 'Ascenseur D_2', 'Ascenseur D_3', 'Ascenseur D_4', 'Ascenseur D_5'),
        ('Ascenseur A_RDJ', 'Ascenseur A_0', 'Ascenseur A_1', 'Ascenseur A_2', 'Ascenseur A_3')
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
    
    
    


    