# ur.s3c - Laboratorio de Ataque a LLMs (OWASP Top 10)

<p align="center">
  <img src="Conferencias URSec.png" alt="ur.s3c Logo" width="300">
  <br>
  <b>Semillero de Investigación en Ciberseguridad - Universidad del Rosario</b>
</p>

---

## 📝 Descripción
Este es un taller práctico diseñado para explorar las vulnerabilidades críticas en aplicaciones basadas en Modelos de Lenguaje de Gran Escala (LLM), alineado con el **OWASP Top 10 for LLMs**. El laboratorio permite experimentar con ataques de **Inyección de Prompt Directa**, **Inyección Indirecta (RAG)** y **Ejecución Excesiva de Agencia (RCE)** en un entorno controlado y contenerizado.

Desarrollado para el taller con **HTB Colombia**, este MVP de 3 niveles utiliza tecnologías modernas para simular un entorno empresarial vulnerable.

---

## 🏗️ Arquitectura del Sistema
El laboratorio está compuesto por los siguientes componentes:

*   **Frontend & Backend:** Aplicación basada en **Python 3.11**, **FastAPI** y **Streamlit**.
*   **Motor de Inferencia:** **Ollama** ejecutando el modelo **Llama 3.2 (1B)**.
*   **Orquestación:** **Docker-Compose** para un despliegue simplificado.
*   **Puerto Expuesto:** La aplicación es accesible a través del **puerto 80**.

---

## 💻 Requerimientos de Hardware
Para garantizar un rendimiento fluido del modelo local, se recomiendan las siguientes especificaciones:

*   **Procesador:** Intel Core i5 / AMD Ryzen 5 o superior.
*   **Memoria RAM:** 8GB (Mínimo) / **10GB (Recomendado)**.
*   **Almacenamiento:** 5GB de espacio libre en disco.
    *   *Nota: El modelo Llama 3.2 (1B) se descarga automáticamente durante el primer arranque si no está presente.*

---

## 🚀 Instrucciones de Despliegue

Existen dos métodos para poner en marcha el laboratorio:

### Método A: Usando el Snapshot (Recomendado ⚡)
Este método es ideal para entornos de taller ya que utiliza una imagen pre-construida.
1.  Importar la imagen:
    ```bash
    docker load -i urs3c-lab-snapshot.tar
    ```
2.  Iniciar los contenedores:
    ```bash
    docker compose up -d
    ```
    *Nota: Este método no requiere internet para los binarios, pero sí es necesaria una conexión para el primer `ollama pull` del modelo.*

### Método B: Compilación desde Código Fuente
Si deseas construir la imagen localmente:
1.  Construir e iniciar:
    ```bash
    docker compose up --build -d
    ```
    *Requiere conexión a internet activa para descargar dependencias y el modelo.*

---

## ⚠️ Primer Arranque (CRÍTICO)
Tras ejecutar el comando de despliegue, la aplicación **puede tardar entre 5 a 10 minutos** en estar totalmente operativa. Durante este tiempo, el contenedor realiza:
1.  Descarga automática del modelo **Llama 3.2 (1B)**.
2.  Configuración inicial y *warm-up* del motor de inferencia.

Puedes monitorear el progreso con el siguiente comando:
```bash
docker logs -f urs3c-lab
```

---

## 🚩 Descripción de los Retos

El laboratorio consta de 3 niveles de dificultad progresiva:

### Nivel 1: Inyección Directa (ASI01)
*   **Objetivo:** Manipular el input del usuario para saltar las restricciones del sistema y extraer la **Flag** oculta en el *System Prompt* del asistente.

### Nivel 2: Inyección Indirecta vía RAG (ASI01 Indirect)
*   **Objetivo:** El sistema utiliza Generación Aumentada por Recuperación (RAG). Debes identificar y aprovechar documentos "envenenados" en la base de conocimientos para forzar al LLM a revelar una **Flag secundaria**.

### Nivel 3: Agencia Excesiva y Path Traversal (ASI04/05)
*   **Objetivo:** El agente tiene acceso a herramientas del sistema. Debes explotar la lógica de ejecución para realizar un **Path Traversal** y leer archivos sensibles del sistema de archivos, específicamente en `../../secret/flag3.txt`, utilizando la función disponible `get_file`.

---

## 🔐 Formato de Flags
Para mantener la integridad del laboratorio, las flags se encuentran ofuscadas en **Base64** dentro del código fuente. Sin embargo, el formato de entrega final para el taller es:
`UR_S3C{texto_de_la_flag}`

---

## ⚖️ Aviso Ético
Este laboratorio ha sido creado con fines estrictamente **educativos y de investigación (CTF)**. El uso de estas técnicas fuera de entornos controlados es ilegal y poco ético. El semillero **ur.s3c** no se hace responsable por el mal uso de esta herramienta.

---
<p align="center">
  <img src="images/BT Bank Logo.png" alt="BT Bank Logo" width="150">
  <br>
  <i>Investigación por ur.s3c - Universidad del Rosario</i>
</p>
