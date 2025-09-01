# 📜 README.md - Prueba Técnica Desarrollador Junior

## 📝 Descripción del Proyecto
Este repositorio contiene la solución a la **Prueba Técnica para Desarrollador Junior en Verticcal**.  
El objetivo principal es demostrar las habilidades necesarias para el desarrollo de actividades diarias, incluyendo el desarrollo de APIs, integración con servicios de terceros, persistencia de datos y automatización de flujos de trabajo.

---

## 💻 Tecnologías Utilizadas
Las siguientes tecnologías fueron utilizadas en este proyecto:

- **Python 3.9+**: Con el framework FastAPI para la creación de la API.  
- **PostgreSQL**: Base de datos para la persistencia de los leads.  
- **n8n**: Automatización de flujos de trabajo de procesamiento de datos, ejecutado a través de Docker en entorno local.  

---
# 🛠️ Instalación y Ejecución
Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

## 1. Configuración del Entorno Python

**Crea un entorno virtual:**  
Abre una terminal en la raíz del proyecto y ejecuta el siguiente comando:

```bash
python -m venv venv
```

**Activa el entorno virtual:**  
Es indispensable que actives el entorno virtual para instalar las dependencias en el lugar correcto.

- En Windows:  
```bash
venv\Scripts\activate
```

- En macOS/Linux:  
```bash
source venv/bin/activate
```

**Instala las dependencias:**  
Una vez activado el entorno, instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

---

## 2. Configuración y Ejecución de n8n con Docker

**Crea el archivo `docker-compose.yml`:**  
Verifica si tienes el archivo `docker-compose.yml` en la raíz del proyecto. Si no lo tienes, usa el siguiente contenido:

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n_container
    ports:
      - '5678:5678'
    volumes:
      - ~/.n8n:/home/node/.n8n
    environment:
      - N8N_EDITOR_URL=http://localhost:5678/
    restart: unless-stopped
```

**Inicia n8n:**  
Abre una terminal en la raíz del proyecto y ejecuta el siguiente comando para levantar el contenedor:

```bash
docker-compose up -d
```

**Importa y activa el flujo de trabajo:**  
- Abre tu navegador y ve a [http://localhost:5678/](http://localhost:5678/).  
- Importa el archivo `Prueba_Verticcal_n8n.json` que está en el proyecto.  
- Una vez importado, activa el flujo para que el webhook comience a escuchar las peticiones.  

**Configura las credenciales de PostgreSQL en n8n:**  
Para que el flujo se conecte a la base de datos, necesitas configurar las credenciales.
- En la interfaz de n8n, buscas los nodos de PostgreSQL.
- Haz clic en el campo Credential y selecciona New.
- Llena los campos con la información de tu base de datos (host, nombre de la base de datos, usuario y contraseña).
- Una vez configurado, el nodo de PostgreSQL estará listo para funcionar.
---

## 3. Ejecución de la API (Backend)

**Inicia la API con FastAPI:**  
Asegúrate de que tu entorno virtual esté activo. Debes navegar a la carpeta `app` y luego ejecutar el comando de FastAPI:

```bash
cd app/
fastapi dev main.py
```

La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).  
Puedes ver la documentación interactiva en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).  
---

## 🚀 Parte A: Manejo de APIs

### 1. Consumo de API Externa
- **API Elegida**: [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts)  
- **Datos Consumidos**: Publicaciones (posts).  
- **Motivo de la elección**: Elegí esta API para simular la interacción con datos de usuarios, lo que permitió un acercamiento práctico al análisis de datos.

### 2. Endpoints de la API Propia
Se crearon los siguientes endpoints para exponer y procesar los datos de la API externa:

- `GET /external-data/posts`  
  Obtiene y devuelve una lista completa de todos los posts de la API externa.

- `GET /external-data/posts/{post_id}`  
  Recupera un post específico utilizando su ID.

- `GET /external-data/posts/filter?field={field}&key_word={keyword}`  
  Permite filtrar los posts por una palabra clave en un campo específico (`title` o `body`).  

### 3. Buenas Prácticas Implementadas
1. **Separación de Responsabilidades**: El proyecto está organizado en módulos (`routers`, `schemas`, `services`) para asegurar modularidad y fácil mantenimiento.  
2. **Inyección de Dependencias**: Uso de dependencias de FastAPI para facilitar reutilización y pruebas unitarias.  
3. **Validación de Datos con Pydantic**: Modelos (`PostDtoRequest`) para asegurar esquemas definidos y datos estandarizados.  
4. **Manejo de Errores**: Excepciones con respuestas HTTP apropiadas (ej. `404 Not Found`).  
5. **Patrón de Abstracción**: Implementación de `GenericUseCase` para estandarizar métodos y mejorar escalabilidad.  
6. **Documentación Automática**: Endpoints documentados con FastAPI, generando Swagger UI interactivo.  

---

## 💾 Parte B: Persistencia de Leads (PostgreSQL)

Para la persistencia de datos se utilizó **PostgreSQL** con una capa de acceso a datos mediante **SQLAlchemy** en modo asíncrono.

### 1. Configuración de la Base de Datos
- **Herramienta de Persistencia**: SQLAlchemy.  
- **Esquema de la Tabla**:  
  - `id`: Identificador único (Primary Key).  
  - `name`: Nombre del lead.  
  - `location`: Ubicación geográfica.  
  - `budget`: Presupuesto asignado (`BigInteger`).  

- **Creación de Tablas**: Script en `scripts/create_tables.py` para automatizar creación de la base de datos y la tabla `leads`.

### 2. Ejecución del script:
#### 1. Crear archivo .env
En la carpeta scripts, crea un archivo llamado `.env` y copia el contenido de `.env.example`. Luego, modifica la cadena de conexión de la base de datos con tus credenciales. Debes cambiar `myuser`, `mypassword` y `mydatabase` por los valores correctos:
```bash
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase

```
### 2. Ejecuta el script:
Abre una terminal, navega hasta la carpeta del proyecto y, con el entorno virtual activado, ejecuta el comando para crear la base de datos.
```bash
cd scripts/
python -m scripts.CreateTables
```
---

## 🤖 Parte C: Automatización con n8n

Se construyó un flujo de trabajo en **n8n** para procesar los leads, exportado en `Prueba_Verticcal_n8n.json`.

### 1. Arquitectura del Flujo
El flujo se inicia con un **Webhook Trigger** que espera a ser llamado. A continuación, la arquitectura de procesamiento es la siguiente:
- **Extracción de Parámetros:** El siguiente nodo extrae los parámetros de la URL del webhook.
- **Limpieza de Datos:** Se utiliza un nodo para eliminar toda la información de la base de datos, específicamente de la tabla `leads`. 
- **Generación de Datos de Prueba**  Un nodo de tipo `Function` retorna un JSON con nuevos valores para insertar. Esta implementación se realizó para fines de prueba, con una posible mejora que consistiría en consultar la base de datos para identificar duplicados y eliminarlos de la lista antes de la inserción.
- **Inserción en PostgreSQL:** Un nodo de PostgreSQL se encarga de insertar el array de información generado por el nodo anterior.
- **Recuperación de Datos:** Un segundo nodo de PostgreSQL consulta y trae toda la información de la tabla `leads`.  
- **Filtrado:** La información se pasa a un nodo de filtrado, donde se aplican los parámetros recibidos por el webhook (query parameters).  
- **Cálculo y Ordenamiento:** Un nodo de tipo `Function` calcula la sumatoria de los presupuestos (`budgets`) y organiza los leads en orden descendente por presupuesto. 
- **Salidas del Flujo:** Esta última función se ramifica en dos salidas:
  - Una para el **Webhook Response**, que devuelve el resultado.
  - Otra para transformar el resultado en un archivo JSON, con el objetivo de permitir la descarga de la información, sirviendo como una base para una futura extensión del flujo.

### 2. Parámetros Aceptados
- `location`: Filtra por ubicación (ej. *Bogotá*, *Medellín*).  
- `budget_min`: Filtra leads con presupuesto ≥ valor.  
- `budget_max`: Filtra leads con presupuesto ≤ valor.  

### 3. Ejemplo de Resultado y URL  
El flujo retorna un objeto JSON con el presupuesto total del conjunto de leads filtrados y una lista de los leads ordenados de mayor a menor presupuesto.  

**Ejemplo de URL para Postman:**  
```
http://localhost:5678/webhook/init-app?location=Medellín&budget_min=200000000
```

**Ejemplo de Payload de Respuesta:**  
```json
{
  "total_budget": 1350000000,
  "sorted_leads": [
    {
      "id": 3,
      "name": "Nicolle Rodríguez",
      "location": "Medellín",
      "budget": "650000000"
    },
    {
      "id": 2,
      "name": "Santiago Gallo",
      "location": "Medellín",
      "budget": "500000000"
    },
    {
      "id": 1,
      "name": "Ana Salcedo",
      "location": "Medellín",
      "budget": "200000000"
    }
  ]
}
```

---

## 🤖 Parte D: Meta-prompt para comunicaciones de Soporte  

Se diseñó un meta-prompt para generar mensajes de soporte técnico claros, empáticos y resolutivos. Este prompt guía a un modelo de lenguaje para producir comunicaciones estructuradas para los clientes en las etapas clave de una incidencia.  

Para ver el prompt completo junto con sus casos de prueba, por favor consulta el archivo `mt-promt.md`.  

### 1. Directrices del Meta-prompt  
El prompt está configurado para que el modelo actúe como un agente de soporte empático y profesional, adhiriéndose a las siguientes directrices:  

- **Recepción**: Confirma la recepción del caso y solicita información faltante de manera cortés.  
- **Diagnóstico**: Explica la causa del problema y las acciones en curso con un tono tranquilizador.  
- **Resolución**: Detalla las acciones clave realizadas y solicita la validación del cliente.  
- **Personalización y Tono**: Utiliza la información del cliente para personalizar el mensaje, manteniendo un tono formal, transparente y sin jerga técnica.  
- **Formato**: Sigue un formato estricto de correo electrónico, con un Asunto y un Cuerpo, e incluye el número de ticket en ambas secciones.  

### 2. Razón del Meta-prompt  
Este meta-prompt se creó con el objetivo de estandarizar y mejorar la calidad de la comunicación con los clientes, garantizando una experiencia de soporte consistente y profesional.  

Las principales razones detrás de su diseño son:  
- **Eficiencia**: Automatiza la redacción de mensajes rutinarios, liberando a los agentes de soporte para que se concentren en la resolución de problemas más complejos.  
- **Consistencia**: Asegura que todos los mensajes, independientemente del agente o del caso, sigan un formato y un tono coherentes, lo que refuerza la imagen de la marca.  
- **Empatía y Transparencia**: Al establecer directrices claras para el tono y la estructura, el prompt ayuda a mantener una comunicación empática y transparente, informando al cliente de manera oportuna sobre el estado de su caso. Esto reduce la ansiedad y aumenta la confianza en el proceso de soporte.  
- **Claridad**: Al exigir el uso de lenguaje sencillo y sin jerga técnica, se garantiza que la información sea accesible y comprensible para todos los clientes, sin importar su nivel de conocimiento técnico.  

