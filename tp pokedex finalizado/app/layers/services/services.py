# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user



# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    
    # debe ejecutar los siguientes pasos:
    cards=[]#lista vacia para las cards
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    imagenes_crudas=transport.getAllImages()#llamamos a la funcion getAllImages desde transport.py 
    #la cual se encarga de obtener las imagenes desde la API de los pokemon.
    
    # 2) convertir cada img. en una card.
    for imagenes in imagenes_crudas:#recorremos cada una de las imagenes.
        card=translator.fromRequestIntoCard(imagenes) #llamamos a la funcion fromRequestIntoCard desde translator.py 
        #la cual se encarga de transformar en cards a cada una de las imagenes de la API.
        cards.append(card)#cada que se crea una card se agrega a la lista vacia cards=[].
     
     # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    return cards #al final toda esta funcion devuelve todas las imagenes convertidas en cards dentro de una lista. 

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []#lista vacia

    for card in getAllImages():
        
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower()==card.name.lower():#verificamos si el name(nombre ingresado por el usuario) 
            #es igual a alguno en las cards de los pokemones.
            
            filtered_cards.append(card)#si un nombre coincide se agrega la card a la lista vacia.

    return filtered_cards#retorna al pokemon ingresado en formato card

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []#lista vacia.

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. 
        # Si es así, se añade al listado de filtered_cards.
        if any(type_filter.lower() == tipo.lower() for tipo in card.types):#verifica si almenos un tipo del pokemon coincide 
            #con el tipo buscado, con el "for" de la condicion recorremos los tipos que posee un pokemon,
            # ya que algunos poseen mas de uno
        
            filtered_cards.append(card)#si el tipo coincide se agrega la card a la lista.

    return filtered_cards#devuelve la o las cards segun el tipo buscado. 

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.
    for pokes in getAllFavourites(request):#recorremos la lista de favoritos. 
        if fav.name==pokes.name: #si el pokemon ya esta en la lista de favoritos, no devuelve nada(no lo agrega porque ya esta).
            return None

    return repositories.save_favourite(fav) #si no esta lo guardamos en la BD.


# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:#si el usuario no esta logueado:
        return []#no devuelve nada.
    else:#si el usuario esta logueado:
        user = get_user(request)#este el usuario.

        lista_favoritos = repositories.get_all_favourites(user) # buscamos desde el repositories.py 
        #TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []#lista vacia

        for favorito in lista_favoritos:#recorremos cada favorito en la lista.
            card = translator.fromRepositoryIntoCard(favorito) # convertimos cada favorito en una Card. 
            
            mapped_favourites.append(card)#lo almacenamos en el listado de mapped_favourites.
        
    return mapped_favourites#devuelve las cards favoritas.



def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)