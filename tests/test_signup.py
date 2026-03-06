"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""
import pytest


class TestSignupHappyPath:
    """Tests for successful signup scenarios."""
    
    def test_signup_new_student_succeeds(self, client, reset_activities):
        """
        Arrange: New student email and existing activity
        Act: POST signup request
        Assert: Student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert email in response_data["message"]
    
    def test_signup_adds_student_to_participants_list(self, client, reset_activities):
        """
        Arrange: New student email
        Act: POST signup request, then fetch activities
        Assert: Student appears in participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        participants = activities_data[activity_name]["participants"]
        assert email in participants
        assert len(participants) == 3  # 2 original + 1 new


class TestSignupErrorCases:
    """Tests for signup error scenarios."""
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Arrange: Nonexistent activity name
        Act: POST signup request to invalid activity
        Assert: Returns 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_student_returns_400(self, client, reset_activities):
        """
        Arrange: Student already signed up for activity
        Act: POST signup request for same student and activity
        Assert: Returns 400 Bad Request
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_does_not_modify_database_on_error(self, client, reset_activities):
        """
        Arrange: Student already signed up
        Act: Attempt duplicate signup
        Assert: Participants list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        original_count = 2
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == original_count
