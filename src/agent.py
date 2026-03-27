import re
import ollama

MODEL = "llama3.2:1b"
OLLAMA_OPTIONS = {
    "num_ctx": 2048,
    "temperature": 0.0,
    "num_predict": 300,
}


def python_repl_telemetry_stub(command: str) -> str:
    print("\n[ALERTA - HONEY-AGENT]")
    print("El LLM intento usar la herramienta con el payload:")
    print("--------------------------------------------------")
    print(command)
    print("--------------------------------------------------")
    print("Estado: Bloqueado (Simulacion Educativa)\n")
    return "Output interceptado y registrado exitosamente por la herramienta de defensa."


def run_agent(message: str) -> str:
    decision_prompt = (
        "Eres un agente con una herramienta llamada PythonREPL.\n"
        "Si necesitas herramienta, responde EXACTAMENTE con:\n"
        "ACTION: PythonREPL\n"
        "INPUT: <comando>\n"
        "Si no necesitas herramienta, responde normalmente."
    )
    decision = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": decision_prompt},
            {"role": "user", "content": message},
        ],
        options=OLLAMA_OPTIONS,
    )["message"]["content"]
    print(f"[DEBUG] Model raw output: {decision}")

    pattern = r"ACTION:\s*PythonREPL\s*\nINPUT:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, decision, flags=re.IGNORECASE | re.DOTALL)
    print(f"[DEBUG] Regex match: {match}")
    if not match:
        return decision

    tool_input = match.group(1).strip()
    tool_output = python_repl_telemetry_stub(tool_input)
    final = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Eres un asistente tecnico. Responde al usuario en espanol."},
            {
                "role": "user",
                "content": (
                    f"Solicitud del usuario:\n{message}\n\n"
                    f"Resultado de la herramienta PythonREPL:\n{tool_output}\n\n"
                    "Genera la respuesta final para el usuario."
                ),
            },
        ],
        options=OLLAMA_OPTIONS,
    )["message"]["content"]
    return final


def main():
    print("=== Iniciando Honey-Agent (ollama only) ===")
    print("Escribe 'salir' para terminar.\n")
    while True:
        try:
            user_input = input("Usuario > ")
            if user_input.lower() in ["salir", "exit", "quit"]:
                break
            response = run_agent(user_input)
            print(f"\nRespuesta Final > {response}\n")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"\n[Error en Inferencia]: {e}\n")


if __name__ == "__main__":
    main()
