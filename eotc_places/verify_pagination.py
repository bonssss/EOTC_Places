import os
import django
from rest_framework.test import APIClient
from rest_framework import status
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eotc_places.settings')
django.setup()

from places.models import HolyPlace

def test_pagination_and_filtering():
    client = APIClient()
    
    # Create some test data
    HolyPlace.objects.all().delete()
    for i in range(15):
        HolyPlace.objects.create(
            name=f"Place {i}",
            location="Test Location",
            region="Test Region",
            description="Test Description",
            history="Test History"
        )
        
    # Test Pagination
    print("Testing Pagination...")
    response = client.get('/places/places/')
    if response.status_code == 200:
        data = response.json()
        if 'count' in data and 'next' in data and 'previous' in data and 'results' in data:
            print("Pagination structure present.")
            if data['count'] == 15 and len(data['results']) == 10:
                print("Pagination count and page size correct.")
            else:
                print(f"Pagination count/size incorrect: count={data['count']}, results={len(data['results'])}")
        else:
            print("Pagination structure missing.")
    else:
        print(f"Failed to get places: {response.status_code}")

    # Test Filtering
    print("\nTesting Filtering...")
    response = client.get('/places/places/?search=Place 1')
    if response.status_code == 200:
        data = response.json()
        # Should match "Place 1", "Place 10", "Place 11", "Place 12", "Place 13", "Place 14" -> 6 items
        # Wait, "Place 1" matches "Place 1" and "Place 10".. "Place 14".
        print(f"Filter results count: {data['count']}")
        if data['count'] > 0:
             print("Filtering returned results.")
        else:
             print("Filtering returned no results.")
    else:
        print(f"Failed to filter places: {response.status_code}")

if __name__ == "__main__":
    test_pagination_and_filtering()
