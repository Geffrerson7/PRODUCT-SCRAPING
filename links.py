import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para almacenar todos los enlaces de las imágenes
enlaces_imagenes_total = []
# Lista para almacenar todos los enlaces de los productos
captions_links = []
# Lista para almacenar todos los SKU de los productos
sku_productos_total = []
base = "https://nav-simplest-prd.ripley.com.pe"

# Iterar sobre los números del 13 al 24
for n in range(13, 25):
    # Construir la URL dinámicamente
    url = f"https://nav-simplest-prd.ripley.com.pe/tienda/supervet-6048558?page={n}"

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los elementos img con el atributo data-src
        imagenes = soup.find_all('img', attrs={'data-src': True})

        # Iterar sobre las imágenes y guardar los enlaces en la lista total
        for img in imagenes:
            enlace = img['data-src']
            enlaces_imagenes_total.append(enlace)

        links = soup.find_all(
            "a", class_="catalog-product-item catalog-product-item__container undefined"
        )
        
        # Extraer los atributos href de los elementos encontrados
        hrefs = [link["href"] for link in links]
        captions_links.extend(hrefs)

        # Imprimir los enlaces encontrados
        for href in hrefs:
            url_product = base + href + "s=mdco"
            response_2 = requests.get(url_product)
            if response_2.ok:
                soup_2 = BeautifulSoup(response_2.text, "html.parser")
                sections = soup_2.find_all('section', class_='product-header visible-xs')
                
                for section in sections:
                    span_element = section.find('span', class_='sku sku-value')
                    # Extraer el texto del elemento <h1>
                    
                    if span_element:
                        product_sku = span_element.text.strip()
                        sku_productos_total.append(product_sku)
    else:
        print(f"Error al realizar la solicitud para la página {n}:", response.status_code)

# Crear un DataFrame de pandas con todos los enlaces de las imágenes
df = pd.DataFrame(enlaces_imagenes_total, columns=['Enlace de la Imagen'])

# Guardar el DataFrame en un archivo Excel
df.to_excel('enlaces_imagenes_total.xlsx', index=False)

print("Los enlaces de las imágenes se han guardado en 'enlaces_imagenes_total.xlsx'")
