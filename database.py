import pymysql
import random

class Database:
  def __init__(self, password_path, db_name):
    with open(password_path) as f:
      password = f.readline().strip('\n')
    self.db = pymysql.connect("localhost", "root", password, db_name,
        cursorclass=pymysql.cursors.DictCursor)
    self.cursor = self.db.cursor()

  def table_insert(self, table_name, attr_names, attrs):
    command = "INSERT INTO %s(%s) VALUES(%s)" % (table_name, ','.join(attr_names),
        ','.join(tuple("'%s'"%(s) if type(s) is str else "%d"%(s) for s in attrs)))
    self.exec(command)

  def table_create(self, table_name, attrs):
   command = 'CREATE TABLE %s (%s)' % (table_name, ','.join([' '.join(attr) for attr in attrs]))
   self.cursor.execute(command)

  def new_table(self, table_name, cols, values):
    self.table_create(table_name, cols)
    attr_names = tuple(x[0] for x in cols[1:] if x[0] != '')
    for v in values:
      self.table_insert(table_name, attr_names, v)

  def exec(self, command):
    try:
      self.cursor.execute(command)
      self.db.commit()
      result = self.cursor.fetchall()
    except:
      print('Error: unable to fetch data')
      self.db.rollback()
      result = None
    return result

  def __del__(self):
    self.db.close()

def create_entity_player(db):
  table_name = 'players'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('name', 'VARCHAR(20)', 'NOT NULL'),
      ('sex', 'CHAR(1)', 'NOT NULL'),
      ('age', 'INT', 'NOT NULL'),
  )
  values = (
      ('Ming', 'M', 15),
      ('Mary', 'F', 20),
      ('John', 'M', 24),
      ('Amy', 'F', 16),
      ('Jane', 'F', 29),
      ('Hito', 'M', 18),
      ('Mos', 'M', 17),
      ('Aaron', 'M', 20),
      ('Ivan', 'M', 33),
      ('Irwin', 'M', 19)
  )
  db.new_table(table_name, cols, values)
  return len(values)

def create_entity_server(db):
  table_name = 'servers'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('name', 'VARCHAR(30)', 'NOT NULL'),
      ('location', 'VARCHAR(30)', 'NOT NULL'),
  )
  locations = ('HongKong', 'Taiwan', 'China', 'Malaysia', 'America', 
      'India', 'Japan', 'Korea', 'Australia', 'NewZealand')
  values = tuple( (s+'_server', s) for s in locations)
  db.new_table(table_name, cols, values)
  return len(values)

def create_entity_game(db):
  table_name = 'games'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('name', 'VARCHAR(30)', 'NOT NULL'),
      ('develop_year', 'INT', 'NOT NULL'),
  )
  values = tuple(('game%d'%(i), 2000+i) for i in range(1,41))
  db.new_table(table_name, cols, values)
  return len(values)

def create_entity_publishers(db):
  table_name = 'publishers'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('name', 'VARCHAR(30)', 'NOT NULL'),
      ('num_employee', 'INT', 'NOT NULL'),
  )
  values = tuple(('publisher_%d'%(i), random.randint(20,100)) for i in range(1,11))
  db.new_table(table_name, cols, values)
  return len(values)

def create_entity_employees(db):
  table_name = 'employees'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('name', 'VARCHAR(30)', 'NOT NULL'),
      ('phone', 'VARCHAR(20)', 'NOT NULL'),
  )
  values = tuple(('employee_%d'%(i), 
    '0918'+''.join([str(random.randint(0,9)) for _ in range(6)])) for i in range(1,26))
  db.new_table(table_name, cols, values)
  return len(values)

def create_relation_player_server_game(db, num_p, num_s, num_g):
  table_name = 'r_play'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('player_id', 'INT', ''),
      ('','','FOREIGN KEY (player_id) REFERENCES players(id)'),
      ('server_id', 'INT', ''),
      ('','','FOREIGN KEY (server_id) REFERENCES servers(id)'),
      ('game_id', 'INT', ''),
      ('','','FOREIGN KEY (game_id) REFERENCES games(id)'),
  )
  games = list(range(1, num_g+1))
  values = list()
  for p in range(1, num_p+1):
    num_game_played = random.randint(1,6)
    games_p_play = random.sample(games, num_game_played)
    values += [(p, random.randint(1,num_s), g) for g in games_p_play]
  db.new_table(table_name, cols, values)

def create_relation_server_employee(db, num_s, num_e):
  table_name = 'r_maintain'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('server_id', 'INT', ''),
      ('','','FOREIGN KEY (server_id) REFERENCES servers(id)'),
      ('employee_id', 'INT', ''),
      ('','','FOREIGN KEY (employee_id) REFERENCES employees(id)'),
  )
  employees = list(range(1, num_e+1))
  values = list()
  for s in range(1, num_s+1):
    num_employee_maintain = random.randint(1,5)
    employees_incharge = random.sample(employees, num_employee_maintain)
    values += [(s, e) for e in employees_incharge]
  db.new_table(table_name, cols, values)

def create_relation_game_publisher(db, num_g, num_p):
  table_name = 'r_publish'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('game_id', 'INT', ''),
      ('','','FOREIGN KEY (game_id) REFERENCES games(id)'),
      ('publisher_id', 'INT', ''),
      ('','','FOREIGN KEY (publisher_id) REFERENCES publishers(id)'),
  )
  values = tuple((g, random.randint(1, num_p)) for g in range(1,num_g+1))
  db.new_table(table_name, cols, values)

def create_relation_player_game(db, num_p, num_g):
  print('close beta')
  table_name = 'r_closed_beta'
  cols = (
      ('id', 'INT', 'PRIMARY KEY AUTO_INCREMENT'),
      ('player_id', 'INT', ''),
      ('','','FOREIGN KEY (player_id) REFERENCES players(id)'),
      ('game_id', 'INT', ''),
      ('','','FOREIGN KEY (game_id) REFERENCES games(id)'),
  )
  players = list(range(1, num_p+1))
  values = list()
  for g in range(1, num_g+1):
    num_closed_player = random.randint(2,5)
    closed_players = random.sample(players, num_closed_player)
    values += [(p, g) for p in closed_players]
  db.new_table(table_name, cols, values)

def main():
  db = Database('password.txt', 'games')
  num_player = create_entity_player(db)
  num_server = create_entity_server(db)
  num_game = create_entity_game(db)
  num_publisher = create_entity_publishers(db)
  num_employee = create_entity_employees(db)
  create_relation_player_server_game(db,
      num_player, num_server, num_game)
  create_relation_server_employee(db,
      num_server, num_employee)
  create_relation_game_publisher(db,
      num_game, num_publisher)
  create_relation_player_game(db, 
      num_player, num_game)

if __name__ == '__main__':
  main()
