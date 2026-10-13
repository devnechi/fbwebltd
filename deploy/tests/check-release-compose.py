#!/usr/bin/env python3

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.")
    sys.exit(2)

path = Path("compose.release.yml")

if not path.is_file():
    sys.exit("FAIL: compose.release.yml is missing")

compose = yaml.safe_load(path.read_text())

assert compose.get("name") == "fbweb", "Incorrect Compose project name"

services = compose.get("services", {})

for service in ("app", "web", "db"):
    assert service in services, f"Missing service: {service}"

for service in ("app", "web"):
    config = services[service]
    assert "image" in config, f"{service} image is missing"
    assert "build" not in config, f"{service} must not build in production"

expected_volumes = {
    "app_storage": "fbweb_app_storage",
    "db_data": "fbweb_db_data",
    "caddy_data": "fbweb_caddy_data",
    "caddy_config": "fbweb_caddy_config",
}

volumes = compose.get("volumes", {})

for name, expected in expected_volumes.items():
    config = volumes.get(name, {})
    assert config.get("external") is True, f"{name} must be external"
    assert config.get("name") == expected, f"Wrong volume name: {name}"

app_volumes = services["app"].get("volumes", [])
web_volumes = services["web"].get("volumes", [])
db_volumes = services["db"].get("volumes", [])

assert "app_storage:/var/www/html/storage" in app_volumes
assert "app_storage:/srv/storage:ro" in web_volumes
assert "db_data:/var/lib/mysql" in db_volumes

assert "caddy_data:/data" in web_volumes
assert "caddy_config:/config" in web_volumes

assert services["web"]["depends_on"]["app"]["condition"] == "service_healthy"

assert services["app"]["depends_on"]["db"]["condition"] == "service_healthy"

assert services["app"].get("healthcheck"), "App healthcheck missing"

assert "MYSQL_ROOT_PASSWORD" in services["db"].get("environment", {})

print("PASS: Release Compose safety checks")
