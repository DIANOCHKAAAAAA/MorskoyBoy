import unittest
from tkinter import *
from main import change_current_label, generate_ships, check_winner


class TestChangeCurrentLabel(unittest.TestCase):
    def test_correct_completing(self):
        self.window = Tk()
        self.player_label = Label(self.window, text='Вы', font=('Helvetica', 16))
        self.computer_label = Label(self.window, text='Компьютер', font=('Helvetica', 16))
        self.current_label = Label(self.window, text='@@@@@@@', font=('Helvetica', 16))
        self.assertEqual(change_current_label(self.player_label, self.computer_label, self.current_label), None)

    def test_wrong_completing(self):
        with self.assertRaises(TypeError):
            change_current_label(None, None, None)
            change_current_label(self.player_label, None, None)
            change_current_label(self.player_label, self.computer_label, None)


class TestGenerateShips(unittest.TestCase):
    def test_correct_completing(self):
        self.assertEqual(len(generate_ships({'x': 10, 'y': 10})), 10)
        self.assertEqual(len(generate_ships({'x': 10, 'y': 10})[0]), 10)
        self.assertEqual(len(generate_ships({'x': 15, 'y': 20})), 20)
        self.assertEqual(len(generate_ships({'x': 15, 'y': 20})[0]), 15)

    def test_wrong_completing(self):
        with self.assertRaises(ValueError):
            generate_ships({'x': 0, 'y': 0})
        with self.assertRaises(ValueError):
            generate_ships({'x': -1, 'y': -1})
        with self.assertRaises(ValueError):
            generate_ships({'x': 5, 'y': 5})
        with self.assertRaises(ValueError):
            generate_ships({'x': 100, 'y': 3})
        with self.assertRaises(ValueError):
            generate_ships({'x': 3, 'y': 100})


class TestCheckWinner(unittest.TestCase):
    def test_true_returning(self):
        self.assertTrue(check_winner({'x': 3, 'y': 3}, [[1 for i in range(3)] for j in range(3)], [[0 for i in range(3)] for j in range(3)]))
        self.assertTrue(check_winner({'x': 3, 'y': 3}, [[0 for i in range(3)] for j in range(3)], [[1 for i in range(3)] for j in range(3)]))
        self.assertTrue(check_winner({'x': 3, 'y': 3}, [[1, 1, 1], [1, 1, 1], [1, 1, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, -1]]))

    def test_false_returning(self):
        self.assertFalse(check_winner({'x': 3, 'y': 3}, [[1 for i in range(3)] for j in range(3)], [[-1 for i in range(3)] for j in range(3)]))
        self.assertFalse(check_winner({'x': 3, 'y': 3}, [[1 for i in range(3)] for j in range(3)], [[0, 0, 0], [0, 0, 0], [0, 0, -1]]))


if __name__ == '__main__':
    unittest.main()
