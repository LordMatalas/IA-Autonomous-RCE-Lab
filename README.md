# IA-Autonomous-RCE-Lab

> **Diseñado para ayudar. Engañado para atacar.**
> *Entorno de Simulación Educativo para el semillero de investigación en ciberseguridad ur.s3c (Universidad del Rosario).*

---

## 🛑 DISCLAIMER LEGAL Y ÉTICO
> **This tool is for educational purposes only. Do not use on systems you do not own.**
> Este repositorio constituye un **Honey-Agent** (Agente Trampa) diseñado estrictamente para investigar, documentar y defender contra vulnerabilidades en aplicaciones LLM, específicamente las documentadas en el OWASP Top 10 for LLMs: **LLM01: Prompt Injection** y **LLM08: Excessive Agency**.
> 
> El objetivo es **capturar telemetría y entender el comportamiento lógico** de un ataque, demostrando la falla de confianza entre el LLM y el Sistema Operativo, para así aplicar medidas de *Sandboxing* y *Output Parsing Validation*. **Bajo ninguna circunstancia debe utilizarse este entorno para realizar ataques reales.**

---

## 🧠 Sobre este Laboratorio

Durante la charla investigativa, analizaremos cómo un Agente Autónomo (ReAct) dotado con herramientas que interactúan con el sistema operativo (como un intérprete de Python o shell) puede ser manipulado mediante lenguaje natural para ejecutar comandos no previstos (Remote Code Execution - RCE).

En lugar de un bot funcionalmente explotable y peligroso, hemos implementado un componente interceptor que registra el intento de ataque (el *payload*), permitiendo el análisis de la inyección sin comprometer la máquina (Host).

## 🚀 Requisitos e Instalación

### 1. Preparar Ollama
La inferencia se realiza de forma local utilizando [Ollama](https://ollama.com/). Asegúrate de tenerlo instalado y tener descargado el modelo `llama3`.

```bash
# Iniciar el servicio de ollama (si no está corriendo)
ollama serve

# Descargar y correr el modelo (en otra terminal)
ollama run llama3
```

### 2. Configurar el Entorno Python
Se requiere **Python 3.10+**.

```bash
# Clonar o ubicarse en la carpeta del repositorio
cd IA-Autonomous-RCE-Lab

# Crear un entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt
```

### 3. Ejecutar el Honey-Agent
Una vez que el modelo de Ollama esté escuchando en `localhost:11434`, inicia el agente:

```bash
python src/agent.py
```

Prueba interactuar con él usando lenguaje natural o inyectando los *payloads* de ejemplo ubicados en la carpeta `payloads/`.

---

## 📸 Demostración
*(Si tienes un GIF o log de cómo el Honey-Agent intercepta un intento de `os.system('id')`, colócalo aquí para enriquecer la presentación).*

---
*Desarrollado para ur.s3c - Investigación en Ciberseguridad.*
