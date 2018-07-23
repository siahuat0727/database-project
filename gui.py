import tkinter as tk
from database import Database
from prettytable import PrettyTable

class Gui(object):
  def __init__(self):
    self.root = tk.Tk()
    self.root.title('DBMS')
    self.db = Database('password.txt', 'games')

    self.btn_queries = {
        'mysql': '',
        'display all player' :  "SELECT * FROM players",
        'MIN MAX AVG of players' : "SELECT MAX(age), MIN(age), AVG(age) FROM players",
        'SELECT FROM WHERE player age < 20' : "SELECT name FROM players WHERE age < 20",
        'INSERT Sharon' :  "INSERT INTO players(name, sex, age) VALUES('Sharon', 'F', 21)",
        'DELETE Sharon' :  "DELETE FROM players WHERE name = 'Sharon'",
        'UPDATE Ming'   :  "UPDATE players SET age=23 WHERE name = 'Ming'",
        'closed beta of game' :     "SELECT p.name, g.name\n" + 
                                    "FROM r_closed_beta as r, players as p, games as g\n" + 
                                    "WHERE g.id = r.game_id AND p.id = r.player_id\n" + 
                                    "ORDER BY g.id",
        'SUM total closed player' : "SELECT SUM(A.num) as total_closed_player\n" +
                                    "FROM\n" +
                                    "(\n" +
                                    "SELECT COUNT(p.id) as num\n" +
                                    "FROM r_closed_beta as r, players as p, games as g\n" +
                                    "WHERE g.id = r.game_id AND p.id = r.player_id\n" +
                                    "GROUP BY g.name\n" +
                                    ") AS A",
        'num_close_beta > 2(HAVING COUNT)' :  "SELECT g.name, COUNT(p.id) \n" + 
                                              "FROM r_closed_beta as r, players as p, games as g \n" + 
                                              "WHERE g.id = r.game_id AND p.id = r.player_id \n" + 
                                              "GROUP BY g.name \n" + 
                                              "HAVING COUNT(p.id) > 2 \n" + 
                                              "ORDER BY COUNT(p.id)",
        'expert employee(IN)' : "SELECT DISTINCT e.name, e.phone \n" + 
                                "FROM  employees as e, r_maintain as rm \n" + 
                                "WHERE e.id = rm.employee_id and rm.server_id IN \n" + 
                                "( \n" + 
                                "   SELECT s.id \n" + 
                                "   FROM r_play as r, servers as s, players as p \n" + 
                                "   WHERE s.id = r.server_id AND p.id = r.player_id \n" + 
                                "   GROUP BY s.id \n" + 
                                "   HAVING COUNT(p.id) > 3\n" + 
                                ")",
        'leisure employee(NOT IN)' :  "SELECT DISTINCT e.name, e.phone \n" + 
                                      "FROM  employees as e, r_maintain as rm \n" + 
                                      "WHERE e.id = rm.employee_id and rm.server_id NOT IN \n" + 
                                      "( \n" + 
                                      "   SELECT s.id \n" + 
                                      "   FROM r_play as r, servers as s, players as p \n" + 
                                      "   WHERE s.id = r.server_id AND p.id = r.player_id \n" + 
                                      "   GROUP BY s.id \n" + 
                                      "   HAVING COUNT(p.id) > 3\n" + 
                                      ")",
        'Japan employee(EXISTS)' :  "SELECT e.name, e.phone \n" + 
                                    "FROM employees as e \n" + 
                                    "WHERE EXISTS \n" + 
                                    "( \n" + 
                                    "   SELECT * \n" + 
                                    "   FROM r_maintain as r, servers as s \n" + 
                                    "   WHERE e.id = r.employee_id and r.server_id = s.id and s.location = 'Japan' \n" + 
                                    ")",
        'Pure not Japan E(NOT EXISTS)' :  "SELECT e.name, e.phone \n" + 
                                          "FROM employees as e \n" + 
                                          "WHERE NOT EXISTS \n" + 
                                          "( \n" + 
                                          "   SELECT * \n" + 
                                          "   FROM r_maintain as r, servers as s \n" + 
                                          "   WHERE e.id = r.employee_id and r.server_id = s.id and s.location = 'Japan' \n" + 
                                          ")",
        }

    # create gui elements
    l_tool = tk.Label(self.root, text="Query tool",bg='deep sky blue')
    self.cur_menu = tk.StringVar(self.root, 'Click to select tool')
    self.menu = tk.OptionMenu(self.root, self.cur_menu,
        *list(self.btn_queries), command=self.menu_fun)
    l_keys = tk.Label(self.root, text="Query keywords", bg='cyan')
    self.query = tk.Text(self.root)
    btn = tk.Button(self.root, text='Query', bg='azure', command=self.btn_fun)
    self.text_result = tk.Text(self.root)
    self.text_btn_query = tk.Text(self.root)

    # layout
    full_stick = tk.W+tk.E+tk.N+tk.S
    l_tool.grid(row=0, column=0, sticky=full_stick)
    self.menu.grid(row=0, column=1, sticky=full_stick)
    l_keys.grid(row=1, column=0, sticky=full_stick)
    self.query.grid(row=1, column=1, sticky=full_stick)
    btn.grid(row=2, column=0, columnspan=2, sticky=full_stick)
    self.text_result.grid(row=0, column=2, rowspan=4, columnspan=2, sticky=full_stick)
    self.text_btn_query.grid(row=3, column=0, columnspan=2, sticky=full_stick)
    self.root.mainloop()

  def btn_fun(self):
    if self.cur_menu.get() == 'mysql':
      self.do_query(self.query.get(1.0, tk.END))
    else:
      self.display_query('please select mysql first')

  def menu_fun(self, text):
    if text == 'mysql':
      self.display_query('enter your query')
    else:
      command = self.btn_queries[text]
      self.do_query(command)
      self.display_query(command)

  def do_query(self, command):
    ret = self.db.exec(command)
    if ret:
      text = PrettyTable(list(ret[0]))
      for r in ret:
        text.add_row(r.values())
    elif ret == None:
      text = 'Wrong query'
    else:
      text = 'No result'
    self.display_result(text)

  def display_result(self, text):
    self.text_result.delete(1.0, tk.END)
    self.text_result.insert(1.0, text)

  def display_query(self, command):
    self.text_btn_query.delete(1.0, tk.END)
    self.text_btn_query.insert(1.0, command)

