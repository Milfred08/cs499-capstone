"""
Animal Shelter CRUD Module for Austin Animal Center Database
Author: Milfred
Course: CS 340
Module: Database Commands and CRUD Python Module

This module provides comprehensive CRUD (Create, Read, Update, Delete) operations
for managing animal records in the Austin Animal Center MongoDB database.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from datetime import datetime

class AnimalShelter(object):
    """
    CRUD operations for Animal collection in MongoDB
    
    This class provides a comprehensive interface for managing animal shelter data
    with robust error handling, input validation, and industry-standard best practices.
    """

    def __init__(self, username='aacuser', password='Password123!', 
                 host='nv-desktop-services.apporto.com', port=30230, 
                 database='AAC', collection='animals'):
        """
        Initialize the AnimalShelter database connection
        
        Args:
            username (str): MongoDB username for authentication
            password (str): MongoDB password for authentication  
            host (str): MongoDB server hostname
            port (int): MongoDB server port number
            database (str): Target database name
            collection (str): Target collection name
            
        Raises:
            Exception: If database connection fails
        """
        try:
            # Construct MongoDB connection string with authentication
            connection_string = f'mongodb://{username}:{password}@{host}:{port}/'
            
            # Initialize MongoDB client with connection timeout
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            self.client.admin.command('ping')
            
            # Set database and collection references
            self.database = self.client[database]
            self.collection = self.database[collection]
            
            print(f"Successfully connected to MongoDB database: {database}")
            
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def create(self, data):
        """
        Create (Insert) operation - Adds a new document to the MongoDB collection
        
        This method inserts a single document into the specified MongoDB database and collection.
        It includes comprehensive input validation and error handling to ensure data integrity.
        
        Args:
            data (dict): Dictionary containing animal record data with required fields
                       Must include at minimum: animal_id, animal_type, breed
                       
        Returns:
            bool: True if insert was successful and acknowledged by MongoDB, False otherwise
            
        Raises:
            Exception: If data parameter is None, empty, or missing required fields
            
        Example:
            >>> shelter = AnimalShelter()
            >>> animal_data = {
            ...     "animal_id": "A123456",
            ...     "animal_type": "Dog", 
            ...     "breed": "Labrador Retriever",
            ...     "name": "Rex"
            ... }
            >>> result = shelter.create(animal_data)
            >>> print(result)  # True
        """
        # Input validation
        if not data:
            raise Exception("Create operation failed: 'data' parameter is empty or None")
        
        if not isinstance(data, dict):
            raise Exception("Create operation failed: 'data' parameter must be a dictionary")
            
        # Validate required fields for animal records
        required_fields = ['animal_id', 'animal_type', 'breed']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise Exception(f"Create operation failed: Missing required fields: {missing_fields}")
        
        try:
            # Add timestamp for record creation tracking
            data['created_timestamp'] = datetime.now()
            
            # Insert document into MongoDB collection
            insert_result = self.collection.insert_one(data)
            
            # Verify insertion was acknowledged by MongoDB
            if insert_result.acknowledged:
                print(f"Successfully created record for animal_id: {data.get('animal_id', 'Unknown')}")
                return True
            else:
                print("Create operation was not acknowledged by database")
                return False
                
        except Exception as e:
            raise Exception(f"Create operation failed: {str(e)}")

    def read(self, query=None, projection=None, limit=0, sort_field=None, sort_order=1):
        """
        Read (Query) operation - Retrieves documents from the MongoDB collection
        
        This method provides flexible querying capabilities with support for projections,
        limiting results, and sorting. It handles empty queries and provides comprehensive
        error handling for robust database operations.
        
        Args:
            query (dict, optional): MongoDB query document. If None, returns all documents
            projection (dict, optional): Fields to include/exclude in results
            limit (int, optional): Maximum number of documents to return (0 = no limit)
            sort_field (str, optional): Field name to sort by
            sort_order (int, optional): Sort direction (1 = ascending, -1 = descending)
            
        Returns:
            list: List of documents matching the query criteria
            
        Raises:
            Exception: If query parameter is not a dictionary or database error occurs
            
        Example:
            >>> shelter = AnimalShelter()
            >>> # Find all dogs
            >>> dogs = shelter.read({"animal_type": "Dog"})
            >>> # Find dogs with specific fields only
            >>> dogs = shelter.read({"animal_type": "Dog"}, {"name": 1, "breed": 1})
        """
        try:
            # Handle empty query - return all documents if no query specified
            if query is None:
                query = {}
            elif not isinstance(query, dict):
                raise Exception("Read operation failed: 'query' parameter must be a dictionary")
            
            # Build the cursor with query
            cursor = self.collection.find(query)
            
            # Apply projection if specified
            if projection and isinstance(projection, dict):
                cursor = self.collection.find(query, projection)
            
            # Apply sorting if specified
            if sort_field:
                cursor = cursor.sort(sort_field, sort_order)
            
            # Apply limit if specified
            if limit > 0:
                cursor = cursor.limit(limit)
            
            # Convert cursor to list and return results
            results = list(cursor)
            
            print(f"Read operation successful: Retrieved {len(results)} document(s)")
            return results
            
        except Exception as e:
            raise Exception(f"Read operation failed: {str(e)}")

    def update(self, query, new_values, upsert=False):
        """
        Update operation - Modifies existing documents in the MongoDB collection
        
        This method updates documents matching the query criteria with new values.
        It uses MongoDB's $set operator to update specific fields while preserving
        other document data. Includes comprehensive validation and error handling.
        
        Args:
            query (dict): MongoDB query document to identify records to update
            new_values (dict): Dictionary of field-value pairs to update
            upsert (bool, optional): If True, create new document if no match found
            
        Returns:
            dict: Update result information including matched_count and modified_count
            
        Raises:
            Exception: If query or new_values parameters are invalid or empty
            
        Example:
            >>> shelter = AnimalShelter()
            >>> update_result = shelter.update(
            ...     {"animal_id": "A123456"},
            ...     {"outcome_type": "Adoption", "outcome_subtype": "Foster"}
            ... )
            >>> print(f"Modified {update_result['modified_count']} document(s)")
        """
        # Input validation
        if not query:
            raise Exception("Update operation failed: 'query' parameter is empty or None")
        
        if not new_values:
            raise Exception("Update operation failed: 'new_values' parameter is empty or None")
            
        if not isinstance(query, dict):
            raise Exception("Update operation failed: 'query' parameter must be a dictionary")
            
        if not isinstance(new_values, dict):
            raise Exception("Update operation failed: 'new_values' parameter must be a dictionary")
        
        try:
            # Add timestamp for update tracking
            new_values['last_modified_timestamp'] = datetime.now()
            
            # Perform update operation using $set operator
            update_result = self.collection.update_many(
                query, 
                {"$set": new_values}, 
                upsert=upsert
            )
            
            # Prepare detailed result information
            result_info = {
                'acknowledged': update_result.acknowledged,
                'matched_count': update_result.matched_count,
                'modified_count': update_result.modified_count,
                'upserted_id': getattr(update_result, 'upserted_id', None)
            }
            
            if update_result.acknowledged:
                print(f"Update successful: {result_info['modified_count']} document(s) modified")
                return result_info
            else:
                print("Update operation was not acknowledged by database")
                return result_info
                
        except Exception as e:
            raise Exception(f"Update operation failed: {str(e)}")

    def delete(self, query, confirm_delete=True):
        """
        Delete operation - Removes documents from the MongoDB collection
        
        This method safely deletes documents matching the query criteria with
        built-in safety measures to prevent accidental data loss. Includes
        comprehensive logging and error handling.
        
        Args:
            query (dict): MongoDB query document to identify records to delete
            confirm_delete (bool): Safety flag to prevent accidental deletions
            
        Returns:
            dict: Delete result information including deleted_count
            
        Raises:
            Exception: If query parameter is invalid, empty, or too broad
            
        Example:
            >>> shelter = AnimalShelter()
            >>> delete_result = shelter.delete({"animal_id": "A123456"})
            >>> print(f"Deleted {delete_result['deleted_count']} document(s)")
        """
        # Input validation
        if not query:
            raise Exception("Delete operation failed: 'query' parameter is empty or None")
            
        if not isinstance(query, dict):
            raise Exception("Delete operation failed: 'query' parameter must be a dictionary")
        
        # Safety check to prevent accidental mass deletions
        if query == {} and confirm_delete:
            raise Exception("Delete operation failed: Empty query would delete all documents. Use confirm_delete=False to override.")
        
        try:
            # Count documents that would be deleted for logging
            count_to_delete = self.collection.count_documents(query)
            
            if count_to_delete == 0:
                print("Delete operation: No documents match the specified query")
                return {'acknowledged': True, 'deleted_count': 0}
            
            # Perform delete operation
            delete_result = self.collection.delete_many(query)
            
            # Prepare detailed result information
            result_info = {
                'acknowledged': delete_result.acknowledged,
                'deleted_count': delete_result.deleted_count
            }
            
            if delete_result.acknowledged:
                print(f"Delete successful: {result_info['deleted_count']} document(s) deleted")
                return result_info
            else:
                print("Delete operation was not acknowledged by database")
                return result_info
                
        except Exception as e:
            raise Exception(f"Delete operation failed: {str(e)}")
    
    def close_connection(self):
        """
        Safely close the MongoDB connection
        
        This method should be called when finished with database operations
        to properly release database resources.
        """
        try:
            self.client.close()
            print("Database connection closed successfully")
        except Exception as e:
            print(f"Error closing database connection: {str(e)}")
    
    def get_collection_stats(self):
        """
        Retrieve collection statistics for monitoring and debugging
        
        Returns:
            dict: Collection statistics including document count and size information
        """
        try:
            stats = self.database.command("collstats", "animals")
            document_count = self.collection.count_documents({})
            
            return {
                'document_count': document_count,
                'collection_size': stats.get('size', 'Unknown'),
                'index_count': stats.get('nindexes', 'Unknown')
            }
        except Exception as e:
            print(f"Error retrieving collection stats: {str(e)}")
            return None

# Example usage and testing functions
if __name__ == "__main__":
    """
    Example usage and basic testing of the AnimalShelter CRUD operations
    This section demonstrates proper usage patterns for each CRUD operation
    """
    
    try:
        # Initialize the shelter database connection
        print("=== Animal Shelter CRUD Operations Demo ===")
        shelter = AnimalShelter()
        
        # Display collection statistics
        stats = shelter.get_collection_stats()
        if stats:
            print(f"Collection contains {stats['document_count']} documents")
        
        # Example test data for demonstration
        test_animal = {
            "animal_id": "TEST123456",
            "animal_type": "Dog",
            "breed": "Golden Retriever",
            "color": "Golden",
            "date_of_birth": "2023-01-15",
            "name": "Buddy",
            "sex_upon_outcome": "Neutered Male",
            "age_upon_outcome_in_weeks": 104.0,
            "outcome_type": "Adoption",
            "outcome_subtype": "Foster"
        }
        
        print("\n=== Testing Create Operation ===")
        create_success = shelter.create(test_animal)
        print(f"Create operation result: {create_success}")
        
        print("\n=== Testing Read Operation ===")
        read_results = shelter.read({"animal_id": "TEST123456"})
        print(f"Found {len(read_results)} matching record(s)")
        
        print("\n=== Testing Update Operation ===")
        update_info = shelter.update(
            {"animal_id": "TEST123456"},
            {"outcome_type": "Return to Owner", "outcome_subtype": ""}
        )
        print(f"Update result: {update_info}")
        
        print("\n=== Testing Delete Operation ===")
        delete_info = shelter.delete({"animal_id": "TEST123456"})
        print(f"Delete result: {delete_info}")
        
        # Close connection properly
        shelter.close_connection()
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
