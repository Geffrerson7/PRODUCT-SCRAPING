import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para almacenar todos los nombres de los productos
nombres_productos_total = []

# Iterar sobre los números del 13 al 24
for n in range(1, 12):
    # Construir la URL dinámicamente
    url = f"https://nav-simplest-prd.ripley.com.pe/tienda/supervet-6048558?page={n}"

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los divs con la clase 'catalog-product-details__name'
        nombres_divs = soup.find_all('div', class_='catalog-product-details__name')

        # Iterar sobre los elementos encontrados y guardar los nombres en la lista total
        for div in nombres_divs:
            nombre = div.text.strip()
            nombres_productos_total.append(nombre)
    else:
        print(f"Error al realizar la solicitud para la página {n}:", response.status_code)

# Crear un DataFrame de pandas con todos los nombres de los productos
df = pd.DataFrame(nombres_productos_total, columns=['Nombre del Producto'])

# Guardar el DataFrame en un archivo Excel
df.to_excel('nombres_productos_total.xlsx', index=False)

print("Los nombres de los productos se han guardado en 'nombres_productos_total.xlsx'")
