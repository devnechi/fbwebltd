#!/usr/bin/env python3
"""Safety tests for the Future Basics / Chatamarketing gateway."""

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class ChataGatewayContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.compose = yaml.safe_load(
            (ROOT / "compose.release.yml").read_text()
        )
        cls.caddyfile = (
            ROOT / "deploy/Caddyfile"
        ).read_text()

    def test_gateway_joins_both_networks(self):
        networks = self.compose["services"]["web"]["networks"]

        self.assertEqual(
            set(networks),
            {"internal", "chata_edge"},
        )

    def test_app_and_database_remain_isolated(self):
        for service in ("app", "db"):
            config = self.compose["services"][service]

            self.assertEqual(
                set(config["networks"]),
                {"internal"},
            )

            self.assertNotIn("ports", config)

    def test_chata_network_is_external(self):
        network = self.compose["networks"]["chata_edge"]

        self.assertTrue(network["external"])
        self.assertEqual(network["name"], "chata_edge")

        self.assertEqual(
            self.compose["networks"]["internal"]["name"],
            "fbweb_internal",
        )

    def test_gateway_public_ports_unchanged(self):
        ports = self.compose["services"]["web"]["ports"]

        self.assertEqual(
            ports,
            ["80:80", "443:443", "443:443/udp"],
        )

    def test_immutable_image_selection_preserved(self):
        for service in ("app", "web"):
            config = self.compose["services"][service]

            self.assertIn("FBWEB_", config["image"])
            self.assertNotIn("build", config)

    def test_future_basics_routes_preserved(self):
        for required in (
            "futurebasics.co.tz, www.futurebasics.co.tz",
            "root * /srv/public",
            "handle /storage/*",
            "root * /srv/storage/app/public",
            "php_fastcgi app:9000",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.caddyfile)

    def test_chata_domain_and_upstream(self):
        self.assertIn(
            "chatamarketing.co.tz, www.chatamarketing.co.tz",
            self.caddyfile,
        )
        self.assertIn(
            "reverse_proxy chata-web:8080",
            self.caddyfile,
        )

    def test_persistent_gateway_storage_preserved(self):
        web_volumes = self.compose["services"]["web"]["volumes"]

        for required in (
            "app_storage:/srv/storage:ro",
            "caddy_data:/data",
            "caddy_config:/config",
        ):
            self.assertIn(required, web_volumes)


if __name__ == "__main__":
    unittest.main()
