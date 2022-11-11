import pytest

def test_that_login():
    with self.client:
        response = self.client.post('login', { username: 'James', password: '007' })
        # success
        assertEquals(current_user.username, 'James')