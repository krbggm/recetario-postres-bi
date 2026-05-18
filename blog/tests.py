import pytest
from django.urls import reverse
from datetime import datetime
from blog.models import Post

@pytest.mark.django_db
def test_publicaciones_status_code(client):
    url = reverse("publicaciones")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_posts_status_code(client):
    url = reverse("api_posts")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_json_status_code(client):
    url = reverse("json_api")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_post_detail_status_code(client):
    post = Post.objects.create(
        titulo="Pastel Test",
        categoria="Pruebas",
        contenido="Delicioso contenido de prueba",
        autor="Karina",
        fecha=datetime.now()
    )
    url = reverse("api_post_detail", args=[post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == post.id

@pytest.mark.django_db
def test_crear_post(client):
    url = reverse("crear_post")
    data = {
        "titulo": "Nuevo postre",
        "categoria": "Galletas",
        "contenido": "Receta secreta",
        "autor": "Chef",
        "fecha": datetime.now()
    }
    response = client.post(url, data)
    assert response.status_code == 302 
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_xss_protection(client):
    url = reverse("crear_post")
    payload = "<script>alert('XSS')</script>"
    response = client.post(url, {
        "titulo": "Test XSS",
        "categoria": "Seguridad",
        "contenido": payload,
        "autor": "Hacker",
        "fecha": datetime.now()
    })
    assert response.status_code == 302
    post = Post.objects.first()
    assert "<script>" in post.contenido

@pytest.mark.django_db
def test_sql_injection_protection(client):
    url = reverse("crear_post")
    payload = "'; DROP TABLE blog_post; --"
    response = client.post(url, {
        "titulo": "Intento SQL",
        "categoria": "Seguridad",
        "contenido": payload,
        "autor": "Hacker",
        "fecha": datetime.now()
    })
    assert response.status_code == 302
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_titulo_no_vacio(client):
    url = reverse("crear_post")
    response = client.post(url, {
        "titulo": "",
        "categoria": "Invalido",
        "contenido": "Algo de texto",
        "autor": "Anónimo",
        "fecha": datetime.now()
    })
    assert Post.objects.count() == 0