import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

sys.path.append(
    "c:\\Users\\pc lenovo\\Documents\\Projet_Personel\\Programme perso\\Game\\src\\main"
)

from entity import Entity


class TestEntity(unittest.TestCase):
    def setUp(self):
        """Set up the Entity object and mock dependencies."""
        self.sprite_mock = MagicMock()
        self.entity = Entity(0, 0, self.sprite_mock, [0.0, 0.0], [1.0, 1.0, 1.0, 1.0])

    def test_varSpeed_with_valid_inputs(self):
        """Test varSpeed with normal inputs to ensure it updates speed correctly."""
        constraint = np.array([0, 0, 0, 8000])
        resistance = 0.5
        push = [0.2, 1.0]
        time = 0.013

        # Setting initial conditions
        self.entity.direction = np.array([1.0, 0.0, 0.0, 0.0])
        self.entity.speed = np.array([0.5, 0.0])

        self.entity.varSpeed(constraint, resistance, push, time)

        # Assertions for updated speed
        expected_speed = np.array([0.49415, 104.0])

        self.assertTrue(np.allclose(self.entity.speed, expected_speed))

    def test_varSpeed_resets_speed_on_exception(self):
        """Test varSpeed to ensure it resets speed to 0 on exception."""
        constraint = "invalid_input"  # Invalid input to trigger an exception
        resistance = 0.5
        push = [0.2, 1.0]
        time = 0.013

        # Redirect stderr to suppress the stack trace output
        with patch("sys.stderr", new_callable=lambda: open(os.devnull, "w")):
            self.entity.varSpeed(constraint, resistance, push, time)

        # Assertions to ensure speed is reset
        self.assertTrue(np.all(self.entity.speed == np.array([0.0, 0.0])))

    def test_varSpeed_flips_entity_on_orientation_change(self):
        """Test varSpeed to ensure the entity flips when orientation changes."""
        constraint = np.array([0, 0, 0, 8000], dtype=float)
        resistance = 0.5
        push = [0.2, 1.0]
        time = 0.013

        # Setting initial conditions
        self.entity.direction = np.array([-1.0, 0.0, 0.0, 0.0])
        self.entity.speed = np.array([1.0, 0.0])
        self.entity.orient = -1

        with patch.object(self.entity, "flip", wraps=self.entity.flip) as flip_mock:
            # Redirect stderr to suppress the stack trace output
            with patch("sys.stderr", new_callable=lambda: open(os.devnull, "w")):
                self.entity.varSpeed(constraint, resistance, push, time)

            # Assert that flip was called
            flip_mock.assert_called_once_with(True, False)

            # Assert orientation change
            self.assertEqual(self.entity.orient, -1)

    def test_varSpeed_does_not_flip_entity_on_same_orientation(self):
        """Test varSpeed to ensure the entity does not flip unnecessarily."""
        constraint = np.array([0, 0, 0, 8000], dtype=float)
        resistance = 0.5
        push = [0.2, 1.0]
        time = 0.013

        # Setting initial conditions
        self.entity.direction = np.array([-1.0, 0.0, 0.0, 0.0])
        self.entity.speed = np.array([1.0, 0.0])
        self.entity.orient = 1

        with patch.object(self.entity, "flip", wraps=self.entity.flip) as flip_mock:
            # Redirect stderr to suppress the stack trace output
            with patch("sys.stderr", new_callable=lambda: open(os.devnull, "w")):
                self.entity.varSpeed(constraint, resistance, push, time)
            # Assert that flip was called
            flip_mock.assert_not_called()

            # Assert orientation change
            self.assertEqual(self.entity.orient, 1)


if __name__ == "__main__":
    unittest.main()
