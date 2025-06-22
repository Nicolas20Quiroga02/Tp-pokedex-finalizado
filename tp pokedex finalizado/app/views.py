# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout




#
def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, 
# ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    
    pokemones=services.getAllImages()#llamamos a la funcion de services(getAllImages) que nos devuleve una 
    #lista con las cards de los pokemon.
    lista_de_favoritos=services.getAllFavourites(request)#llamamos a la funcion de services(getAllFavourites) 
    #que nos devuleve una lista con las cards de los pokemon favoritos del usuario logueado.
    return render(request, 'home.html', { 'images': pokemones ,'favourite_list':lista_de_favoritos  })#devuelve a la pagina 
    #cada card de los pokemon


# función utilizada en el buscador.
def search(request):#
    name = request.POST.get('query', '')#nombre del pokemon solicitado por el usuario.
    card_solicitada=services.filterByCharacter(name)#pedimos a la funcion de service que 
    #busque entre todas las cards al pokemon solicitado.
    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (card_solicitada!=[]) :#si la busqueda coincide con algun pokemon, se agrega a la lista ese mismo.
        pokemon_solicitado = card_solicitada#agrega al pokemon a la lista
        favourite_list = card_solicitada#agrega al pokemon a la lista
        


        return render(request, 'home.html', { 'images':pokemon_solicitado, "favourite_list":favourite_list })#devuelve 
        #la card del pokemon buscado
    else:#si el nombre que ingreso el ususario no coincide con algun pokemon, nos devuelve a "home"(pagina principal)
        return redirect("home")

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')
    type_card=services.filterByType(type)

    if type_card != []:#si el tipo del pokemon coincide:
        images = type_card #agrega a la lista los pokemones que coinciden con el tipo solicitado.
        favourite_list = type_card#agrega a la lista los pokemones que coinciden con el tipo solicitado.

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })#devuelve la lista de los pokemon.
    else:#si no coincide ningun tipo:
        return redirect('home')#regresa a la pagina principal(galeria).

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list=services.getAllFavourites(request)#devuelve la lista de favoritos.
    return render(request,"favourites.html",{'favourite_list': favourite_list })#muestra los favoritos en la pagina.
    

@login_required
def saveFavourite(request):
    guardar=services.saveFavourite(request)  # Guarda el favorito
    # Después de guardar, redirige a home.html
    return redirect('home')

    
@login_required
def deleteFavourite(request):
    borrar_list=services.deleteFavourite(request)
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list,  'borrar_list': borrar_list })
    

@login_required
def exit(request):
    logout(request)
    return redirect('home')
