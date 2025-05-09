import json
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
        
        # Start database transaction
        with db.session.begin():
            # Get existing franchises and locations
            existing_franchises = {f.name: f for f in Franchise.query.all()}
            existing_locations = {l.name: l for l in Location.query.all()}
            
            # Update or create franchises
            for franchise_name in franchise_names:
                if franchise_name in existing_franchises:
                    current_app.logger.debug(f"Franchise already exists: {franchise_name}")
                else:
                    franchise = Franchise(name=franchise_name)
                    db.session.add(franchise)
                    current_app.logger.debug(f"Added new franchise: {franchise_name}")
            
            # Update or create locations and franchise-location relationships
            for franchise_name, locations in franchise_locations.items():
                franchise = Franchise.query.filter_by(name=franchise_name).first()
                if not franchise:
                    current_app.logger.debug(f"Warning: Franchise not found in database: {franchise_name}")
                    continue
                
                # Get existing locations for this franchise
                existing_franchise_locations = {
                    fl.location.name for fl in 
                    FranchiseLocation.query.filter_by(franchise_id=franchise.id).all()
                }
                
                # Add new locations and relationships
                for location_name in locations:
                    # Create location if it doesn't exist
                    if location_name not in existing_locations:
                        location = Location(name=location_name)
                        db.session.add(location)
                        existing_locations[location_name] = location
                        current_app.logger.debug(f"Added new location: {location_name}")
                    
                    location = existing_locations[location_name]
                    
                    # Create franchise-location relationship if it doesn't exist
                    if location_name not in existing_franchise_locations:
                        franchise_location = FranchiseLocation(
                            franchise_id=franchise.id,
                            location_id=location.id
                        )
                        db.session.add(franchise_location)
                        current_app.logger.debug(
                            f"Added relationship: {franchise_name} - {location_name}"
                        )
            
            # Remove franchise-location relationships that no longer exist
            for franchise in Franchise.query.all():
                if franchise.name in franchise_locations:
                    current_locations = set(franchise_locations[franchise.name])
                    existing_relationships = FranchiseLocation.query.filter_by(
                        franchise_id=franchise.id
                    ).all()
                    
                    for relationship in existing_relationships:
                        location = Location.query.get(relationship.location_id)
                        if location.name not in current_locations:
                            db.session.delete(relationship)
                            current_app.logger.debug(
                                f"Removed relationship: {franchise.name} - {location.name}"
                            )
            
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
        
        current_app.logger.debug("Database population completed successfully")
        
    except Exception as e:
        current_app.logger.error(f"Error populating database: {str(e)}")
        raise
