mymapping = {
    
    "properties":{
        "context":{
            "type":"text"
        },
        "date-vectorisation":{
            "type":"text"
        },
        "Lien":{
            "type":"text"
        },
        "Titre":{
            "type":"text"
        },
        "version":{
            "type":"text"
        },
        "context_vector":{
            "type":"dense_vector",
            "dims":384,
            "index":True,
            "similarity":"l2_norm"
            
        }
        
        
        
    }
    
    
}