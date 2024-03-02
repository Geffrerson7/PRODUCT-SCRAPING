import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para almacenar todos los SKU de los productos
sku_productos_total = []
# Diccionario para almacenar los enlaces de las imágenes por SKU
enlaces_imagenes_por_sku = {}
base = "https://nav-simplest-prd.ripley.com.pe"

# Iterar sobre los números del 13 al 24
for n in range(37, 39):
    # Construir la URL dinámicamente
    url = f"https://nav-simplest-prd.ripley.com.pe/tienda/supervet-6048558?page={n}"

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all(
            "a", class_="catalog-product-item catalog-product-item__container undefined"
        )

        # Extraer los atributos href de los elementos encontrados
        hrefs = [link["href"] for link in links]

        # Imprimir los enlaces encontrados
        for href in hrefs:
            url_product = base + href + "s=mdco"
            response_2 = requests.get(url_product)
            if response_2.ok:
                soup_2 = BeautifulSoup(response_2.text, "html.parser")
                sku_sections = soup_2.find_all(
                    "section", class_="product-header visible-xs"
                )
                ul_element = soup_2.find("ul", class_="product-image-previews")

                for sku_section in sku_sections:
                    span_element = sku_section.find("span", class_="sku sku-value")

                    if span_element:
                        product_sku = span_element.text.strip()
                        sku_productos_total.append(product_sku)
                        enlaces_imagenes_por_sku.setdefault(product_sku, [])
                        # Verificar si se encontró el elemento ul
                        if ul_element:
                            # Encontrar todos los elementos img dentro del elemento ul
                            imagenes = ul_element.find_all(
                                "img", attrs={"data-src": True}
                            )
                            # Iterar sobre las imágenes y guardar los enlaces en la lista por SKU
                            for img in imagenes:
                                enlace = img["data-src"]
                                # Agregar prefijo "https://" si no lo tiene
                                if not enlace.startswith("https://"):
                                    enlace = "https:" + enlace
                                enlaces_imagenes_por_sku[product_sku].append(enlace)
                        else:
                            print("No se encontraron elementos de imagen en la página.")

    else:
        print(
            f"Error al realizar la solicitud para la página {n}:", response.status_code
        )


# Convertir el diccionario a una lista de tuplas para crear el DataFrame
data = [(sku, ",".join(enlaces_imagenes_por_sku[sku])) for sku in sku_productos_total]

# Crear un DataFrame de pandas con los enlaces de imágenes y los SKU
df = pd.DataFrame(data, columns=["SKU", "link"])

# Guardar el DataFrame en un archivo Excel
df.to_excel("enlaces_imagenes_y_sku_4.xlsx", index=False)

print(
    "Los enlaces de las imágenes y los SKU se han guardado en 'enlaces_imagenes_y_sku.xlsx'"
)
