import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para almacenar todos los nombres de los productos
nombres_productos_total = []
# Lista para almacenar todos los SKU de los productos
sku_productos_total = []
# Lista para almacenar todos los enlaces de los productos
captions_links = []

# URL base de la página web
base_url = "https://nav-simplest-prd.ripley.com.pe/tienda/supervet-6048558?page={}"
base = "https://nav-simplest-prd.ripley.com.pe"

# Iterar sobre las páginas de 1 a 37
for page_num in range(1, 38):
    # URL de la página web actual
    url = base_url.format(page_num)

    # Realizar la solicitud GET a la página web
    response = requests.get(url)
    if response.ok:
        # Parsear el contenido HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar todos los elementos <a> con la clase específica y otros atributos
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
                    # Encontrar el elemento <h1> dentro de cada <section>
                    h1_element = section.find('h1')
                    span_element = section.find('span', class_='sku sku-value')
                    # Extraer el texto del elemento <h1>
                    if h1_element:
                        product_name = h1_element.text.strip().title()
                        nombres_productos_total.append(product_name)
                    if span_element:
                        product_sku = span_element.text.strip()
                        sku_productos_total.append(product_sku)
    
# Crear DataFrames
df_nombre = pd.DataFrame(nombres_productos_total, columns=['Nombre del Producto'])
df_sku = pd.DataFrame(sku_productos_total, columns=['SKU'])
df_caption_link = pd.DataFrame(captions_links, columns=['Caption Link'])                

# Concatenar los DataFrames
df_final = pd.concat([df_nombre, df_sku, df_caption_link], axis=1)

# Guardar el DataFrame combinado en un archivo Excel
df_final.to_excel('productos-supervet-final.xlsx', index=False)