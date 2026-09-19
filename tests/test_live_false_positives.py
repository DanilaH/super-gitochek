import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curate_catalog import classify, exclusion_reason


class ObservedFalsePositivesTest(unittest.TestCase):
    def test_hardware_simulator_is_not_a_game(self):
        item = {"full_name": "wokwi/avr8js", "description": "Arduino (8-bit AVR) simulator, written in JavaScript and runs in the browser"}
        self.assertEqual(classify(item)[0], "other")
        self.assertIsNone(exclusion_reason(item))

    def test_socket_dependent_bomberman_is_not_standalone(self):
        item = {"full_name": "Grohden/ts-phaser-bomb-game", "description": "Bomberman clone using websockets and phaser 3"}
        self.assertEqual(classify(item)[0], "complex_game")
        self.assertIsNone(exclusion_reason(item))

    def test_framework_port_is_a_tool(self):
        item = {"full_name": "littlee/wechat-small-game-phaser", "description": "make phaser works with wechat small game"}
        self.assertEqual(classify(item)[0], "tool")
        self.assertIsNone(exclusion_reason(item))

    def test_external_crypto_dependency_is_not_simple_adaptation(self):
        item = {"full_name": "apoorvlathey/Crypto-Car-Battle", "description": "NFT (ERC721) based HTML5 game with Crypto Payouts"}
        self.assertEqual(classify(item)[0], "complex_game")
        self.assertIsNone(exclusion_reason(item))

    def test_real_small_games_remain(self):
        for item in [
            {"full_name": "ssusnic/Pseudo-3d-Racer", "description": "A javascript racing game tutorial on making a complete pseudo 3d racer"},
            {"full_name": "megbrimef/urso-slot-base", "description": "Slot base game"},
        ]:
            self.assertEqual(classify(item)[0], "game")
            self.assertIsNone(exclusion_reason(item))


if __name__ == "__main__":
    unittest.main()
