# Library
import unittest
from typer.testing import CliRunner
# local
from to_do.cli import __app_name__, __version__, app
from to_do.To_Do import ToDo

class TestMyCli(unittest.TestCase):
    
    def test_create_command(self):
        runner = CliRunner()
        result = runner.invoke(
            app, ["create", "Buy groceries", "--done-by", "20/02/2023"]
        )
        self.assertIn("data was successfully saved", result.stdout)
    
    def test_show_command(self):
        runner = CliRunner()
        result = runner.invoke(app, ["show"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("To Do", result.stdout)
    
    def test_delete_command(self):
        runner = CliRunner()
        todo = ToDo()
        all_todo = todo.all()
        todo_id = all_todo[0]["id"]
        result = runner.invoke(app, ["delete", f"{todo_id}"])
        self.assertIn(f"has been delete", result.stdout)

    def test_update_command(self):
        runner = CliRunner()
        todo = ToDo()
        all_todo = todo.all()
        todo_id = all_todo[0]["id"]
        result = runner.invoke(app, ["update", f"{todo_id}","--name","buy new things","--done-by", "20/03/2023"])
        self.assertIn(f"data was successfully updated", result.stdout)

if __name__ == '__main__':
    unittest.main()
