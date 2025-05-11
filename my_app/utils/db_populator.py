from pathlib import Path
from flask import current_app
from my_app import db
from my_app.models import Franchise, Location, FranchiseLocation

def populate_database():
    """
    Populates the database with franchise and location data from text files.
    This function is called during app initialization.
    """
    current_app.logger.debug("Starting database population...")
    
    # Get the path to the static assets directory
    static_dir = Path(current_app.static_folder) / 'assets'
    
    try:
        # Read franchise names
        with open(static_dir / 'bbt_franchises.txt', 'r') as f:
            franchise_names = [line.strip() for line in f if line.strip()]
        
        # Read location data
        with open(static_dir / 'bbt_locations.txt', 'r') as f:
            location_data = f.read()
        
        # Parse location data into a dictionary
        franchise_locations = {}
        current_franchise = None
        
        for line in location_data.split('\n'):
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
        
        # STEP 1: Process franchises and locations
        # Use session.add() without transaction blocks for adding
        
        # Get existing franchises and locations
        existing_franchises = {f.name: f for f in Franchise.query.all()}
        existing_locations = {l.name: l for l in Location.query.all()}
        
        # Update or create franchises
        for franchise_name in franchise_names:
            if franchise_name not in existing_franchises:
                franchise = Franchise(name=franchise_name)
                db.session.add(franchise)
                current_app.logger.debug(f"Added new franchise: {franchise_name}")
        
        # Create any new locations
        all_locations = set()
        for locations in franchise_locations.values():
            all_locations.update(locations)
            
        for location_name in all_locations:
            if location_name not in existing_locations:
                location = Location(name=location_name)
                db.session.add(location)
                current_app.logger.debug(f"Added new location: {location_name}")
        
        # Commit changes to ensure all franchises and locations have IDs
        db.session.commit()
        
        # STEP 2: Refresh our data from the database
        existing_franchises = {f.name: f for f in Franchise.query.all()}
        existing_locations = {l.name: l for l in Location.query.all()}
        
        # STEP 3: Process franchise-location relationships
        # Get all current relationships for faster comparison
        existing_relationships = {}
        for fl in FranchiseLocation.query.all():
            franchise = Franchise.query.get(fl.franchise_id)
            location = Location.query.get(fl.location_id)
            if franchise and location:
                if franchise.name not in existing_relationships:
                    existing_relationships[franchise.name] = set()
                existing_relationships[franchise.name].add(location.name)
        
        # Add new relationships
        for franchise_name, locations in franchise_locations.items():
            franchise = existing_franchises.get(franchise_name)
            if not franchise:
                current_app.logger.debug(f"Warning: Franchise not found in database: {franchise_name}")
                continue
            
            franchise_relations = existing_relationships.get(franchise_name, set())
            
            for location_name in locations:
                location = existing_locations.get(location_name)
                if not location:
                    current_app.logger.debug(f"Warning: Location not found in database: {location_name}")
                    continue
                
                # Only create if relationship doesn't exist
                if location_name not in franchise_relations:
                    franchise_location = FranchiseLocation(
                        franchise_id=franchise.id,
                        location_id=location.id
                    )
                    db.session.add(franchise_location)
                    current_app.logger.debug(f"Added relationship: {franchise_name} - {location_name}")
        
        # Remove relationships that no longer exist
        for fl in FranchiseLocation.query.all():
            franchise = Franchise.query.get(fl.franchise_id)
            location = Location.query.get(fl.location_id)
            
            if franchise and location:
                if (franchise.name in franchise_locations and 
                    location.name not in franchise_locations[franchise.name]):
                    db.session.delete(fl)
                    current_app.logger.debug(f"Removed relationship: {franchise.name} - {location.name}")
        
        # Commit all relationship changes
        db.session.commit()
        
        # STEP 4: Clean up unused entities
        # Remove locations that are no longer associated with any franchise
        for location in Location.query.all():
            if not FranchiseLocation.query.filter_by(location_id=location.id).first():
                db.session.delete(location)
                current_app.logger.debug(f"Removed unused location: {location.name}")
        
        # Remove franchises that no longer exist in the text file
        for franchise in Franchise.query.all():
            if franchise.name not in franchise_names:
                db.session.delete(franchise)
                current_app.logger.debug(f"Removed franchise: {franchise.name}")
        
        # Final commit
        db.session.commit()
        
        current_app.logger.debug("Database population completed successfully")
        
    except Exception as e:
        # Rollback any pending transactions in case of error
        db.session.rollback()
        current_app.logger.error(f"Error populating database: {str(e)}")
        raise