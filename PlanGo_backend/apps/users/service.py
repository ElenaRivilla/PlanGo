



def split_full_name(full_name):
    name_parts = full_name.strip().split()
    match len(name_parts):
        case 4:  # Dos nombres y dos apellidos
            first_name = name_parts[1] 
            last_name = " ".join(name_parts[2:])
            
        case 3:  # Un nombre y dos apellidos
            first_name = name_parts[0]  
            last_name = " ".join(name_parts[1:]) 
            
        case 2:  # Un nombre y un apellido
            first_name = name_parts[0] 
            last_name = name_parts[1]
            
        case _:  # Caso por defecto (1 palabra o vacío)
            first_name = name_parts[0] if name_parts else ''
            last_name = ''
    return first_name, last_name