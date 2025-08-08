import os
from datetime import datetime

# Configuración de logs
LOG_DIR = "mitm_logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_to_file(filename, data):
    """Guarda datos en un archivo de log."""
    with open(os.path.join(LOG_DIR, filename), "a", encoding="utf-8") as f:
        f.write(data + "\n")

def log_request(flow):
    """Registra detalles de una solicitud HTTP."""
    log_entry = (
        f"\n=== Solicitud Interceptada ===\n"
        f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"URL: {flow.request.pretty_url}\n"
        f"Método: {flow.request.method}\n"
        f"Encabezados:\n"
    )
    for key, value in flow.request.headers.items():
        log_entry += f"  {key}: {value}\n"
    if flow.request.content:
        log_entry += f"Cuerpo: {flow.request.content.decode('utf-8', errors='replace')}\n"
    log_to_file("requests.log", log_entry)

def log_response(flow):
    """Registra detalles de una respuesta HTTP."""
    log_entry = (
        f"\n=== Respuesta Interceptada ===\n"
        f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"URL: {flow.request.pretty_url}\n"
        f"Código de Estado: {flow.response.status_code}\n"
        f"Encabezados de Respuesta:\n"
    )
    for key, value in flow.response.headers.items():
        log_entry += f"  {key}: {value}\n"
    if flow.response.content:
        log_entry += f"Cuerpo de Respuesta: {flow.response.content.decode('utf-8', errors='replace')}\n"
    log_to_file("responses.log", log_entry)

def handle_specific_urls(flow):
    """Filtra y registra tráfico de URLs específicas."""
    target_domains = ["example.com", "api.example.com"]  # Añade tus dominios aquí
    if any(domain in flow.request.pretty_url for domain in target_domains):
        log_entry = (
            f"\n=== Tráfico Específico Interceptado ===\n"
            f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"URL: {flow.request.pretty_url}\n"
            f"Método: {flow.request.method}\n"
        )
        log_to_file("specific_traffic.log", log_entry)

def request(flow):
    log_request(flow)
    handle_specific_urls(flow)

def response(flow):
    log_response(flow)
