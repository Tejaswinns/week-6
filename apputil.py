import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Genius:
    """
    A class to interact with the Genius API.
    """
    
    def __init__(self, access_token):
        """
        Initialize the Genius class with an access token.
        
        This constructor sets up the Genius API client by storing the access token
        that will be used for all subsequent API calls.
        
        Parameters
        ----------
        access_token : str
            The Genius API access token obtained from genius.com/api-clients
            This token authenticates all requests to the Genius API
        """
        # STORE the access token as an instance variable
        # This allows all methods in this class to use the same token
        self.access_token = access_token
    
    def get(self, search_term, per_page=15):
        """
        Collect data from the Genius API by searching for `search_term`.
        
        **Assumes ACCESS_TOKEN is loaded in environment.**

        Parameters
        ----------
        search_term : str
            The name of an artist, album, etc.
        per_page : int, optional
            Maximum number of results to return, by default 15

        Returns
        -------
        list
            All the hits which match the search criteria.
        """
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={os.environ['ACCESS_TOKEN']}&per_page={per_page}"
        
        response = requests.get(genius_search_url)
        json_data = response.json()
        
        return json_data['response']['hits']
    
    def get_artist(self, search_term):
        """
        Get artist information for a search term.
        
        This method:
        1. Searches for the search_term using the Genius search API
        2. Extracts the Primary Artist ID from the first hit
        3. Uses the artist API to get detailed artist information
        4. Returns the artist information dictionary
        
        Parameters
        ----------
        search_term : str
            The name of an artist to search for
            
        Returns
        -------
        dict
            Dictionary containing the artist information from the API
        """
        # STEP 1: Search for the artist using stored access token
        search_url = f"http://api.genius.com/search?q={search_term}&" + \
                    f"access_token={self.access_token}&per_page=15"
        response = requests.get(search_url)
        json_data = response.json()
        hits = json_data['response']['hits']
        
        # Check if we got any search results
        if not hits:
            return None  # No results found, return None
        
        # STEP 2: Extract the Primary Artist ID from the first hit
        # Get the first (most relevant) result from the search hits
        first_hit = hits[0]
        # Navigate through the JSON structure to get the primary artist's ID
        # Structure: hit['result']['primary_artist']['id']
        artist_id = first_hit['result']['primary_artist']['id']
        
        # STEP 3: Use helper method to get detailed artist information
        artist_info = self._get_artist_details(artist_id)
        
        return artist_info

    def _get_artist_details(self, artist_id):
        """
        Helper method to get detailed artist information given an artist ID.
        
        Args:
            artist_id (int): The Genius artist ID
            
        Returns:
            dict: Artist information from Genius API
        """
        # Build the artist-specific URL using the artist ID
        artist_url = f"http://api.genius.com/artists/{artist_id}?" + \
                    f"access_token={self.access_token}"
        
        # Make API call to get detailed artist information
        artist_response = requests.get(artist_url)
        # Convert the artist response to JSON format
        artist_json = artist_response.json()
        
        # Return the artist information dictionary
        return artist_json['response']['artist']

    def get_artists(self, search_terms):
        """
        Get artist information for multiple search terms and return as DataFrame.
        
        Uses the get_artist method to retrieve information for each search term
        and compiles the results into a pandas DataFrame.
        
        Parameters
        ----------
        search_terms : list
            List of artist names to search for
            
        Returns
        -------
        pandas.DataFrame
            DataFrame with columns: search_term, artist_name, artist_id, followers_count
        """
        # Initialize an empty list to store results for each artist
        results = []
        
        # Loop through each search term in the provided list
        for search_term in search_terms:
            try:
                # REUSE Exercise 2: Call our get_artist method for this search term
                # This will do all the API calls and return artist info dictionary
                artist_info = self.get_artist(search_term)
                
                # Check if we successfully got artist information
                if artist_info:
                    # EXTRACT the specific fields we need for our DataFrame
                    # Use .get() method with defaults in case fields are missing
                    artist_name = artist_info.get('name', 'Unknown')  # Artist's name
                    artist_id = artist_info.get('id', None)  # Genius artist ID
                    followers_count = artist_info.get('followers_count', 0)  # Number of followers
                    
                    # CREATE a dictionary with all required columns for this row
                    results.append({
                        'search_term': search_term,  # Original search term
                        'artist_name': artist_name,  # Artist name from API
                        'artist_id': artist_id,      # Genius artist ID
                        'followers_count': followers_count  # Follower count
                    })
                else:
                    # HANDLE CASE: No results found for this search term
                    # Still add a row to maintain DataFrame structure
                    results.append({
                        'search_term': search_term,
                        'artist_name': 'Not Found',  # Indicate no results
                        'artist_id': None,
                        'followers_count': 0
                    })
                    
            except Exception as e:
                # HANDLE ERRORS: API failures, network issues, etc.
                # Add error row to maintain DataFrame structure
                results.append({
                    'search_term': search_term,
                    'artist_name': 'Error',  # Indicate an error occurred
                    'artist_id': None,
                    'followers_count': 0
                })
        
        # CONVERT our list of dictionaries to a pandas DataFrame
        # This gives us the required tabular format with proper columns
        return pd.DataFrame(results)