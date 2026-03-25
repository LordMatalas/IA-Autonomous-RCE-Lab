import warnings
from langchain_community.llms import Ollama
from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain_core.prompts import PromptTemplate

# Ignorar warnings de Langchain para mantener la terminal limpia
warnings.filterwarnings("ignore")

# ==========================================
# HONEY-AGENT / HERRAMIENTA VULNERABLE (STUB)
# ==========================================
def python_repl_telemetry_stub(command: str) -> str:
    """
    Simula la ejecución de comandos de PythonREPL/os.system.
    En un entorno real vulnerable (Excessive Agency), la salida del LLM 
    se pasaría directamente a `exec()` o un shell. Para este laboratorio,
    actuamos como un interceptor para estudiar la telemetría del ataque.
    """
    print(f"\n[🚨 ALERTA - HONEY-AGENT 🚨]")
    print(f"El LLM intentó usar la herramienta con el siguiente payload:")
    print(f"--------------------------------------------------")
    print(f"{command}")
    print(f"--------------------------------------------------")
    print(f"Estado: Bloqueado (Simulación Educativa)\n")
    
    return "Output interceptado y registrado exitosamente por la herramienta de defensa."

def main():
    print("=== Iniciando Honey-Agent (ur.s3c) ===")
    print("Conectando con Ollama (llama3) en localhost:11434...")
    
    # 1. Configurar el LLM
    try:
         llm = Ollama(model="llama3", base_url="http://localhost:11434")
    except Exception as e:
         print(f"Error al conectar con Ollama: {e}")
         return

    # 2. Configurar la herramienta "peligrosa"
    tools = [
        Tool(
            name="PythonREPL",
            func=python_repl_telemetry_stub,
            description="A Python shell. Use this to execute python commands. Input should be a valid python command."
        )
    ]

    # 3. Definir el Prompt Base (ReAct)
    template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)

    # 4. Crear el Agente y el Ejecutor
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, # Verbose en True para ver la "falla de confianza" y el razonamiento del LLM
        handle_parsing_errors=True
    )

    print("\n[✓] Agente listo. Escribe 'salir' para terminar la ejecución.\n")
    
    # 5. Loop de Interacción
    while True:
        try:
            user_input = input("\nUsuario > ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                break
            
            response = agent_executor.invoke({"input": user_input})
            print(f"\nRespuesta Final > {response.get('output', '')}\n")
            
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"\n[Error en Inferencia]: {e}\n")

if __name__ == "__main__":
    main()
