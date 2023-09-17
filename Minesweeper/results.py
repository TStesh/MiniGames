from datetime import datetime
from sqlite3 import connect

class Results:

    def __init__(self):
        self.conn = connect("minesweeper.db")
        self.cur = self.conn.cursor()

    # создать таблицу рекордов
    def create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS results(name VARCHAR(20), "
            "skill INT, duration INT, last_dt TEXT, PRIMARY KEY(name, skill))"
        )

    # mode = true: новая запись
    # mode = false: обновление существующей записи
    def put_record(self, name: str, skill: int, duration: int, mode: bool):
        dt = datetime.now().isoformat(timespec='minutes')
        if mode:
            self.cur.execute(
                'INSERT INTO results VALUES(?, ?, ?, datetime(?))',
                (name, skill, duration, dt)
            )
        else:
            self.cur.execute(
                'UPDATE results SET duration=?, last_dt=datetime(?) WHERE name=? AND skill=?',
                (duration, dt, name, skill)
            )
        self.conn.commit()

    # Сохранить запись в случае рекорда
    def save_rec(self, name: str, skill: int, duration: int):
        r = self.cur.execute(
            'SELECT duration FROM results WHERE name=? AND skill=?', (name, skill)
        )
        d = r.fetchall()
        # d либо нет, либо выглядит как [(duration,)] ->
        # d[0] = (duration,) -> d[0][0] = duration
        if not d:
            self.put_record(name, skill, duration, True)
        elif d[0][0] > duration:
            self.put_record(name, skill, duration, False)

    # Очистить таблицу рекордов
    def clear_records(self):
        self.cur.execute("DROP TABLE IF EXISTS results")
        self.conn.commit()
        self.create_table()

    # Вернуть записи из таблицы
    def get_records(self):
        r = self.cur.execute('SELECT * FROM results')
        return r.fetchall()

    # Вывести в консоль таблицу рекордов
    def show_records(self):
        skill_name = ('Новичок', 'Опытный', 'Эксперт')
        r = self.cur.execute('SELECT * FROM results')
        recs = r.fetchall()
        print('{:^20} | {:^7} | {} | {}'.format('NAME', 'SKILL', 'DURATION', 'LAST_DT'))
        for rec in recs:
            a, b, c, d = rec[0], skill_name[rec[1]], str(rec[2]), rec[3]
            print('{:>20} | {:>7} | {:>8} | {}'.format(a, b, c, d))
        print()


if __name__ == '__main__':
    db = Results()
    db.save_rec('Julia', 2, 100)
    db.save_rec('Julia', 2, 50)
    db.show_records()
