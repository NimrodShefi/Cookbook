from cookbook import create_app

def test_to_home_url_redirect(client):
    response = client.get('/')
    assert response.status_code == 302 # indicates a redirect
    assert '/home' in response.headers['Location']

def test_home_page(client):
    response = client.get('/home')
    assert b'Latest Recipes' in response.data