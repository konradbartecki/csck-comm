import unittest

from config import config


class ConfigTests(unittest.TestCase):
    def test_can_create_config(self):
        config = config()
        self.assertEqual(config.Mode, config.Mode.Client)
        self.assertEqual(config.WorkingDirectory, "./tmp")

    def test_can_read_from_json_client(self):
        self.assertEqual(True, False)

    def test_can_read_from_json_server(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
