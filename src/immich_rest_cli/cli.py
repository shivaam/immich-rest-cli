import os
from pathlib import Path
from openapi_cli_gen import build_cli

# Base URL: override via IMMICH_REST_CLI_BASE_URL env var, fall back to spec default
_base_url = os.environ.get("IMMICH_REST_CLI_BASE_URL") or "http://localhost:2283/api"

# SSL config — all optional, all driven by env vars so generated CLIs work the same way:
#   IMMICH_REST_CLI_VERIFY_SSL=false  → skip cert verification (self-signed/internal)
#   IMMICH_REST_CLI_CA_CERT=/path     → verify against a custom CA bundle
#   IMMICH_REST_CLI_CLIENT_CERT=/path + IMMICH_REST_CLI_CLIENT_KEY=/path → mTLS
_verify_env = os.environ.get("IMMICH_REST_CLI_VERIFY_SSL", "true").strip().lower()
_ca_cert = os.environ.get("IMMICH_REST_CLI_CA_CERT")
if _verify_env in ("false", "0", "no"):
    _verify = False
elif _ca_cert:
    _verify = _ca_cert
else:
    _verify = True

_client_cert_path = os.environ.get("IMMICH_REST_CLI_CLIENT_CERT")
_client_key_path = os.environ.get("IMMICH_REST_CLI_CLIENT_KEY")
if _client_cert_path and _client_key_path:
    _client_cert = (_client_cert_path, _client_key_path)
elif _client_cert_path:
    _client_cert = _client_cert_path
else:
    _client_cert = None

app = build_cli(
    spec=Path(__file__).parent / "spec.yaml",
    name="immich-rest-cli",
    base_url=_base_url,
    verify_ssl=_verify,
    client_cert=_client_cert,
)


def main():
    app()


if __name__ == "__main__":
    main()
