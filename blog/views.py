from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post
from datetime import datetime

# 1. Vista principal
def publicaciones(request):
    posts = Post.objects.all().order_by('-fecha')
    return render(request, 'blog/publicaciones.html', {'posts': posts})

# 2. Vista para crear una nueva receta 
def crear_post(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        categoria = request.POST.get("categoria", "").strip()
        contenido = request.POST.get("contenido", "")
        autor = request.POST.get("autor", "").strip()

        if not titulo:
            return render(request, "blog/crear.html", {
                "error": "¡El nombre del postre no puede estar vacío, bebé!"
            })

        Post.objects.create(
            titulo=titulo, 
            categoria=categoria if categoria else "Postre", 
            contenido=contenido, 
            autor=autor if autor else "Anónimo"
        )
        return redirect("publicaciones")
        
    return render(request, 'blog/crear.html')

# --- ENDPOINTS DE LA API ---

def api_posts(request):
    posts = Post.objects.all().values('id', 'titulo', 'categoria', 'contenido', 'fecha', 'autor')
    return JsonResponse(list(posts), safe=False)

def api_post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    data = {
        'id': post.id,
        'titulo': post.titulo,
        'categoria': post.categoria,
        'contenido': post.contenido,
        'fecha': post.fecha,
        'autor': post.autor,
    }
    return JsonResponse(data)

def api_json(request):
    return render(request, 'blog/api.html')