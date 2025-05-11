def populate_database():
    """
    Populates the database with franchise and location data from text files.
    This function is called during app initialization.
    """
    
    # Read franchise names
    with open('../static/assets/bbt_franchises.txt', 'r') as f:
        franchise_names = [line.strip() for line in f if line.strip()]

    # Read location data
    with open('../static/assets/bbt_locations.txt', 'r') as f:
        location_data = f.read()
    
    # Parse location data into a dictionary
    franchise_locations = {}
    current_franchise = None
    for line in location_data.split('\n'):
        print(line)
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('['):
            continue
        elif line.endswith(']'):
            continue
        elif line in franchise_names:
            # This is a franchise name
            current_franchise = line
            franchise_locations[current_franchise] = []
        else:
            # This is a location
            location = ''.join(c for c in line if c not in ['"', ','])
            if current_franchise:
                franchise_locations[current_franchise].append(location)
    
    for i, j in franchise_locations.items():
        print (i)

populate_database()

