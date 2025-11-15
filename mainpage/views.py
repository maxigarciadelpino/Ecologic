from django.shortcuts import render
from django.http import JsonResponse
import requests

def puntos_verdes_cercanos(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if not lat or not lon:
        return JsonResponse({"error": "Faltan parámetros"}, status=400)
    radio = 20000  

    # Overpass api
    query = f"""
    [out:json][timeout:25];
    (
      node(around:{radio},{lat},{lon})["amenity"="recycling"];
      node(around:{radio},{lat},{lon})["recycling_type"];
      way(around:{radio},{lat},{lon})["amenity"="recycling"];
    );
    out center tags;
    """

    url = "https://overpass-api.de/api/interpreter"
    respuesta = requests.post(url, data={"data": query})
    datos = respuesta.json()

    puntos = []
    for elemento in datos.get("elements", []):
        tags = elemento.get("tags", {})

        nombre = tags.get("name")
        calle = tags.get("addr:street")
        comuna = tags.get("addr:city") or tags.get("addr:suburb")
        tipo = tags.get("recycling_type") or tags.get("amenity")

        # nombre del punto verde
        if not nombre:
            if calle and comuna:
                nombre = f"Punto de reciclaje en {calle}, {comuna}"
            elif calle:
                nombre = f"Punto de reciclaje en {calle}"
            elif comuna:
                nombre = f"Punto de reciclaje en {comuna}"
            elif tipo:
                nombre = f"Centro de reciclaje ({tipo})"
            else:
                nombre = "Punto Verde sin nombre"

        # Coordenadas
        if "lat" in elemento and "lon" in elemento:
            lat_punto = elemento["lat"]
            lon_punto = elemento["lon"]
        elif "center" in elemento:
            lat_punto = elemento["center"]["lat"]
            lon_punto = elemento["center"]["lon"]
        else:
            continue

        puntos.append({
            "nombre": nombre,
            "lat": lat_punto,
            "lon": lon_punto,
        })

    return JsonResponse({"puntos": puntos})

def maps_view(request):
    return render(request, "maps.html")

def home(request):
    return render(request,"init.html")

def about_view(request):
    return render(request,"about.html")
