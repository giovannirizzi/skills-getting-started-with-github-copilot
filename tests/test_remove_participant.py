"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern."""
import pytest


class TestRemoveParticipantHappyPath:
    """Tests for successful participant removal scenarios."""
    
    def test_remove_existing_participant_succeeds(self, client, reset_activities):
        """
        Arrange: Existing participant in activity
        Act: DELETE request to remove participant
        Assert: Request succeeds with 200 status
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert email in response_data["message"]
    
    def test_remove_participant_updates_list(self, client, reset_activities):
        """
        Arrange: Participant is in Chess Club (2 participants)
        Act: DELETE request to remove participant, then fetch activities
        Assert: Participant removed from list (1 participant remains)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        participants = activities_data[activity_name]["participants"]
        assert email not in participants
        assert len(participants) == 1
        assert "daniel@mergington.edu" in participants


class TestRemoveParticipantErrorCases:
    """Tests for participant removal error scenarios."""
    
    def test_remove_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Arrange: Nonexistent activity name
        Act: DELETE request for nonexistent activity
        Assert: Returns 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_nonexistent_participant_returns_404(self, client, reset_activities):
        """
        Arrange: Valid activity, but participant not in it
        Act: DELETE request for participant not in activity
        Assert: Returns 404 Not Found
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notasignup@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found in this activity" in response.json()["detail"]
    
    def test_remove_does_not_modify_database_on_error(self, client, reset_activities):
        """
        Arrange: Participant not in activity
        Act: Attempt to remove nonexistent participant
        Assert: Participants list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notasignup@mergington.edu"
        original_count = 2
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == original_count
