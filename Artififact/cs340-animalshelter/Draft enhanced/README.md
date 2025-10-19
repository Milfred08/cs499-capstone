# CS 340 Project Two: Grazioso Salvare Animal Rescue Dashboard

**Student:** Milfred  
**Course:** CS 340 - Client/Server Development  
**Institution:** Southern New Hampshire University  
**Project:** Interactive Web Application Dashboard  

## Project Overview

### Required Functionality

This project delivers a comprehensive web application dashboard for Grazioso Salvare, an international rescue-animal training company. The dashboard enables users to identify and categorize dogs suitable for search-and-rescue training by integrating with the Austin Animal Center database through a custom CRUD Python module.

### Key Features Implemented

- **Interactive Filtering Options:** Radio button controls for different rescue types (Water, Mountain/Wilderness, Disaster/Individual Tracking)
- **Dynamic Data Table:** Responsive table with sorting, filtering, and pagination capabilities
- **Geolocation Chart:** Interactive map displaying selected animal locations using Leaflet mapping
- **Breed Distribution Chart:** Visual representation of breed distributions in filtered data
- **CRUD Database Integration:** Seamless connection to MongoDB using the Project One CRUD module

## Tools and Technologies Used

### MongoDB Database Integration

**Why MongoDB was selected as the model component:**

- **Document-Based Structure:** MongoDB's document model perfectly matches the complex, varying structure of animal shelter records with multiple optional fields
- **Flexible Schema:** Allows for easy addition of new animal attributes without requiring database schema modifications
- **Query Performance:** Excellent performance for the complex filtering queries required by Grazioso Salvare's rescue type specifications
- **Scalability:** Can handle large datasets from multiple animal shelters as the organization expands
- **JSON-like Documents:** Natural integration with Python data structures and web application frameworks

### Dash Framework Selection

**Why Dash was chosen for the view and controller structure:**

- **Python-Native:** Allows for seamless integration with the existing CRUD Python module without requiring additional language skills
- **Reactive Components:** Built-in callback system provides real-time updates between dashboard components
- **Professional UI Components:** Includes pre-built interactive elements like data tables, charts, and maps that meet enterprise standards
- **Plotly Integration:** Advanced charting capabilities for data visualization requirements
- **Deployment Flexibility:** Can be easily deployed to web servers for client access

### Additional Resources and Software

- **Pandas:** Data manipulation and analysis for processing MongoDB query results
- **Dash Leaflet:** Interactive mapping capabilities for geolocation visualization
- **Plotly Express:** Statistical chart generation for breed distribution analysis
- **PyMongo:** MongoDB driver for database connectivity (integrated in CRUD module)

## Installation and Setup

### Prerequisites

```bash
# Required Python packages
pip install dash
pip install dash-leaflet
pip install plotly
pip install pandas
pip install pymongo
pip install jupyter-dash
```

### Database Requirements
- **MongoDB Access:** Connection to the Austin Animal Center database on Apporto
- **CRUD Module:** AnimalShelter.py file from Project One in the same directory
- **Authentication:** aacuser account credentials properly configured

### File Structure
```
project/
├── ProjectTwoDashboard.ipynb    # Main dashboard application
├── AnimalShelter.py             # CRUD Python module
├── README.md                    # This documentation
└── Grazioso Salvare Logo.png    # Optional logo file
```

## Project Development Steps

### Step 1: Database Query Development

Developed specialized database queries using the CRUD Python module to match Grazioso Salvare's rescue type requirements:

```python
# Water Rescue Query
query = {
    "animal_type": "Dog",
    "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
    "sex_upon_outcome": "Intact Female",
    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
}

# Mountain/Wilderness Rescue Query  
query = {
    "animal_type": "Dog",
    "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
    "sex_upon_outcome": "Intact Male",
    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
}

# Disaster Rescue Query
query = {
    "animal_type": "Dog", 
    "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
    "sex_upon_outcome": "Intact Male",
    "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
}
```

### Step 2: Interactive Dashboard Development

Created responsive web interface components including radio button filters, dynamic data tables, and interactive charts with real-time callback functionality.

### Step 3: Integration and Testing

Integrated all components using the Model-View-Controller (MVC) design pattern with comprehensive testing of all interactive features.

## Usage Instructions

### Running the Dashboard

1. **File Setup:**
   - Place `ProjectTwoDashboard.ipynb` in your working directory
   - Ensure `AnimalShelter.py` is in the same directory
   - Optional: Add `Grazioso Salvare Logo.png` for logo display

2. **Database Connection:**
   - Verify MongoDB server accessibility on Apporto
   - Confirm aacuser account credentials are properly configured
   - Test CRUD module functionality independently if needed

3. **Launch Dashboard:**
   - Open Jupyter Notebook environment
   - Navigate to `ProjectTwoDashboard.ipynb`
   - Run all cells in sequence from top to bottom
   - Wait for "Successfully loaded X records" confirmation message

4. **Access Dashboard:**
   - Dashboard will automatically launch in Jupyter environment
   - Alternative: Navigate to the provided URL (typically http://127.0.0.1:8060/)
   - Dashboard should display with Grazioso Salvare branding and all interactive components

### Testing Functionality

- Test each radio button filter (Water, Mountain, Disaster, Reset)
- Verify data table updates with appropriate animal records
- Select individual rows to test geolocation map updates
- Confirm breed distribution chart reflects current filtered data
- Test sorting, filtering, and pagination features in data table

## Challenges and Solutions

### Challenge 1: Database Query Optimization

**Issue:** Complex filtering queries with multiple criteria were initially slow with large datasets.

**Solution:** Implemented efficient MongoDB queries using compound indexes and optimized the CRUD module's query structure to leverage MongoDB's native filtering capabilities.

### Challenge 2: Real-time Dashboard Updates

**Issue:** Ensuring seamless updates between filtering options, data table, and visualization components.

**Solution:** Utilized Dash's callback system with proper input/output dependencies to create responsive, interconnected dashboard components.

### Challenge 3: Geolocation Data Handling

**Issue:** Some animal records contained missing or invalid latitude/longitude coordinates.

**Solution:** Implemented robust error handling with fallback to Austin, TX coordinates and data validation to ensure map functionality remains stable.

## Screenshots and Demonstration


<img width="1269" height="323" alt="image" src="https://github.com/user-attachments/assets/b8713e80-eca7-4262-820c-ed9ef4776500" />



<img width="1259" height="503" alt="image" src="https://github.com/user-attachments/assets/13f2aa1c-d27d-44b0-9c6b-79558cbb1e0d" />


<img width="1253" height="589" alt="image" src="https://github.com/user-attachments/assets/36587bb8-e867-4b87-8a62-1d8c5d873b64" />


## Troubleshooting

### Common Issues

- **Port Conflicts:** If dashboard fails to start, change port number in final cell: `app.run_server(debug=True, port=8061)`
- **Database Connection:** Verify MongoDB credentials and server accessibility. Check AnimalShelter.py functionality independently
- **Missing Dependencies:** Install all required packages using pip. Restart Jupyter kernel after installation
- **Logo Display:** If logo doesn't appear, ensure file is named exactly "Grazioso Salvare Logo.png" in working directory

## Project Deliverables

### Submitted Files
- **ProjectTwoDashboard.ipynb:** Complete dashboard application with all interactive components
- **AnimalShelter.py:** CRUD Python module from Project One with enhanced functionality
- **README.md:** This comprehensive documentation file
- **Screenshots:** Seven screenshots demonstrating all dashboard functionality

### Technical Achievements
- **Model-View-Controller Architecture:** Clean separation of database operations, user interface, and business logic
- **Industry-Standard Code:** Well-commented, modular code following Python best practices
- **Responsive Design:** Dashboard components that adapt to user interactions and data changes
- **Error Handling:** Robust error management for database connections, data processing, and user interface updates
- **Performance Optimization:** Efficient queries and data processing for smooth user experience

## Technology Stack

- **Backend:** Python 3.7+, PyMongo, Custom CRUD Module
- **Frontend:** Dash Framework, Plotly, Dash Leaflet
- **Database:** MongoDB (Austin Animal Center Dataset)
- **Visualization:** Plotly Express, Interactive Maps
- **Development Environment:** Jupyter Notebook

## Architecture

### Model-View-Controller (MVC) Pattern
- **Model:** MongoDB database with CRUD Python module handling data operations
- **View:** Dash components providing interactive user interface
- **Controller:** Callback functions managing user interactions and data flow

### Data Flow
1. User selects rescue type filter
2. Controller triggers MongoDB query through CRUD module
3. Model returns filtered data
4. View components update with new data (table, map, charts)

## Future Enhancements

- Advanced filtering options with multiple criteria
- User authentication and session management
- Data export capabilities
- Mobile-responsive design improvements
- Real-time data updates from shelter APIs

## Contact Information

**Student:** Milfred Martinez  
**Course:** CS340-Client/Server Development  
**Institution:** Southern New Hampshire University  
**Project:** Grazioso Salvare Animal Rescue Dashboard

## License

This project is developed as part of CS 340 coursework at Southern New Hampshire University.

---

*This dashboard successfully demonstrates mastery of database systems concepts, client-server development, and interactive web application design as required for CS 340 Project Two.*
