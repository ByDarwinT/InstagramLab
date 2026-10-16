# InstagramLab: extracción de datos de Instagram con Python

**Proyecto académico | Séptimo semestre de Ingeniería en Sistemas**

## ¿De qué trata mi proyecto?

InstagramLab es un programa que desarrollé para obtener información visible de perfiles de Instagram y guardarla en un archivo JSON. Mi intención fue poner en práctica lo aprendido sobre *web scraping*, automatización de navegadores y organización de datos. Quería que el programa no se limitara a conseguir enlaces de publicaciones, sino que también recuperara información general del perfil y se pudiera usar sin depender tanto de la consola.

Para desarrollarlo consulté documentación, ejemplos y repositorios públicos en GitHub. A partir de esas referencias fui probando ideas, adaptando partes del código y agregando soluciones según los problemas que encontraba. Mi trabajo se enfocó en entender el proceso, hacer cambios funcionales y ordenar el proyecto para poder explicarlo y mantenerlo.

## ¿Qué hace actualmente?

Al ingresar un usuario o el enlace de su perfil, la aplicación abre Instagram con Playwright y utiliza una sesión autenticada. Después intenta extraer el nombre de usuario, el nombre visible, la biografía, la cantidad de seguidores y seguidos, el número total de publicaciones y la foto de perfil. También permite indicar cuántas publicaciones quiero revisar; de cada una recupera el enlace y los datos disponibles, como descripción, fecha, imágenes y algunas métricas visibles.

Al finalizar, toda la información se guarda en **JSON**, separando los datos del perfil de los de sus publicaciones. Algunos valores pueden quedar vacíos (`null`) cuando Instagram no los muestra o el programa no logra encontrarlos.

Además del modo consola, añadí un **panel web local** desde el cual puedo iniciar una extracción y obtener el resultado. Ahora puedo arrancar la aplicación con un solo comando: `python main.py`.

## Herramientas que utilicé

- **Python:** para la lógica del programa, las funciones y el manejo de archivos.
- **Playwright y Chromium:** para abrir Instagram, navegar y localizar elementos de una página que cambia dinámicamente.
- **Flask:** para conectar el programa con la interfaz web.
- **HTML, CSS y JavaScript:** para construir el formulario, mostrar el avance y comunicarlo con el servidor.
- **JSON:** para almacenar los resultados de forma organizada.
- **Git y GitHub:** para consultar soluciones, organizar versiones y publicar el proyecto.

Una diferencia que aprendí es que **Playwright no es lo mismo que Scrapy**. Ambos se pueden usar en proyectos de extracción de datos, pero en este caso trabajé con Playwright porque necesitaba controlar un navegador real y manejar páginas dinámicas. Tampoco debe confundirse con Pyright, que es una herramienta de análisis de código Python.

## Dificultades que tuve y cómo las resolví

Uno de los primeros retos fue **mantener la sesión de Instagram**. Tener que iniciar sesión constantemente hacía incómodas las pruebas, por lo que trabajé con cookies para recuperar la sesión cuando seguía siendo válida.

Otro problema fue la **biografía**: el programa obtenía correctamente varios datos del perfil, pero ese campo aparecía siempre como `null`. Revisé la lógica de búsqueda de elementos y cambié cómo se elegía el texto, porque podían aparecer varios candidatos en la página. Después incorporé la extracción y descarga de la **foto de perfil**, para no depender únicamente de su enlace.

También encontré dificultades con las **dependencias de Python**. Al instalar el proyecto en Windows, una versión antigua de Playwright provocó un error relacionado con `greenlet` y Python 3.13. Lo resolví actualizando los requisitos del proyecto. Este detalle me hizo entender que un programa puede funcionar en una computadora y fallar en otra por las versiones instaladas.

Finalmente, quise mejorar la forma de utilizar el scraper. Antes todo se ejecutaba desde la terminal. Separé las responsabilidades del código y añadí Flask para que la extracción pudiera iniciarse desde una página web, manteniendo también una opción por consola.

## Cómo está organizado

La carpeta `instagram_lab` contiene los módulos principales: `auth.py` maneja la sesión; `scraper.py` se encarga de extraer datos; `service.py` coordina los pasos; y `config.py` reúne la configuración. `main.py` inicia la aplicación, mientras que `web.py`, `templates` y `static` corresponden a la interfaz.

Esta separación me ayudó a entender mejor dónde hacer cambios sin modificar todo el programa.

## Cómo ejecutarlo

Necesito Python, las dependencias de `requirements.txt` y Chromium instalado mediante Playwright. En Windows, desde la carpeta del proyecto, los comandos son:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Luego debo crear un archivo `.env` a partir de `.env.example` y colocar allí las credenciales de la cuenta utilizada. **Ese archivo y las cookies no se deben publicar en GitHub.** Para iniciar el panel web ejecuto:

```powershell
python main.py
```

## Lo que aprendí y qué mejoraría

Este proyecto me permitió practicar más que la extracción de datos. Aprendí a leer y modificar código, depurar selectores, trabajar con sesiones, manejar errores, guardar resultados y conectar un programa Python con una interfaz. También entendí que Instagram puede cambiar su estructura y que ningún scraper de este tipo tiene resultados garantizados en todos los perfiles.

Como siguiente mejora me gustaría **extraer y almacenar las listas de cuentas que siguen al perfil y las cuentas que el perfil sigue**, no solo sus cantidades. Para hacerlo tendría que estudiar la carga progresiva de esas listas, los límites de acceso y cómo evitar duplicados. Por ahora, esa funcionalidad **no está implementada**.

Considero que el mayor avance fue pasar de un programa que recopilaba enlaces a una aplicación más completa y ordenada. Todavía hay detalles por mejorar, pero ahora comprendo mucho mejor qué hace cada parte y por qué fue necesario desarrollarla así.

## Referencias consultadas

- [Documentación de Playwright para Python](https://playwright.dev/python/)
- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Python](https://docs.python.org/3/)
- Repositorios y ejemplos públicos de GitHub consultados durante el desarrollo (agregar enlaces y atribuciones aplicables antes de publicar).
