"""Cliente local de IT Support API para terminales de Windows."""

import argparse
import base64
import binascii
import http.client
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta la API local de soporte.")
    parser.add_argument("operation", choices=("health", "categories", "priorities", "analyze"))
    parser.add_argument("--port", type=int, choices=range(1, 65536), metavar="PUERTO", default=8000)
    args = parser.parse_args()

    headers = {"Accept": "application/json"}
    body = None
    if args.operation == "analyze":
        try:
            payload = base64.b64decode(sys.stdin.buffer.read().strip(), validate=True)
            body = json.dumps(json.loads(payload.decode("utf-8")), ensure_ascii=False).encode("utf-8")
        except (binascii.Error, ValueError) as exc:
            print(f"Entrada Base64/JSON UTF-8 invalida: {exc!r}", file=sys.stderr)
            return 2
        headers["Content-Type"] = "application/json; charset=utf-8"

    path = "/health" if args.operation == "health" else f"/tickets/{args.operation}"
    connection = http.client.HTTPConnection("127.0.0.1", args.port, timeout=10)
    try:
        connection.request("POST" if body is not None else "GET", path, body=body, headers=headers)
        response = connection.getresponse()
        result = {"StatusCode": response.status, "Body": json.loads(response.read().decode("utf-8"))}
    except (OSError, http.client.HTTPException, ValueError) as exc:
        print(f"No se pudo leer la respuesta JSON de la API local: {exc!r}", file=sys.stderr)
        return 1
    finally:
        connection.close()

    # Escapes JSON ASCII para evitar la conversion implicita de bytes de PowerShell 5.1.
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
