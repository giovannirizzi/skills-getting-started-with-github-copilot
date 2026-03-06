"""Tests for GET /activities and GET / endpoints using AAA pattern."""
import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Response contains all activities
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities_data = response.json()
        assert len(activities_data) == 3
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data
        assert "Gym Class" in activities_data
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        activity = activities_data["Chess Club"]
        
        # Assert
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_get_activities_includes_participants(self, client, reset_activities):
        """
        Arrange: Client is ready, Chess Club has 2 participants
        Act: Make GET request to /activities
        Assert: Participants list is populated
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        chess_participants = activities_data["Chess Club"]["participants"]
        
        # Assert
        assert len(chess_participants) == 2
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants


class TestRootRedirect:
    """Tests for the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Make GET request to /
        Assert: Response redirects to /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
