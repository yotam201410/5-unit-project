import sqlite3
from typing import *
import hashlib


def get_amount_of_question_marks(rows_name: Tuple) -> str:
    returned_str = ""
    for i in rows_name:
        if returned_str == "":
            returned_str += '(?, '
        else:
            returned_str += '?, '
    returned_str = returned_str[0:-2]
    returned_str += ')'
    return returned_str


def remove_quotation(tup: Tuple) -> str:
    returned_str = ""
    for i in tup:
        if returned_str == "":
            returned_str += '('
        returned_str += f"{i}, "
    returned_str = returned_str[0:-2]
    returned_str += ')'
    return returned_str


def add_question_mark_and_equals(rows_names: Tuple) -> str:
    returned_str = ''
    for row_name in rows_names:
        returned_str += f"{row_name} = ? , "
    return returned_str[0:-2]


def handle_columns_names_types_and_constrains(names_types_and_constrains: List[Tuple[str, ...]]) -> str:
    return_str = ""
    for column in names_types_and_constrains:
        if return_str == "":
            return_str += '('
        return_str += f"{column[0]} {column[1]} {column[2]}, "

    return return_str[0:-2] + ')'


class SQLClient(object):
    def __init__(self, db_file_name: str):
        self.db = sqlite3.connect(db_file_name, check_same_thread=False)

    def get_data_from_table(self, table_name: str, where: str = None, variables: Tuple | Dict = None,
                            amount_to_fetch: int = 0,
                            data_to_select: str = "*") -> List | Any:
        cursor = self.db.cursor()
        if variables is None:
            result = cursor.execute(f"select {data_to_select} from {table_name} {where if where is not None else ''}")
        else:
            result = cursor.execute(f"select {data_to_select} from {table_name} {where if where is not None else ''}",
                                    variables)

        return result.fetchall() if amount_to_fetch == 0 else result.fetchone() if amount_to_fetch == 1 else result.fetchmany(
            amount_to_fetch)

    def add_data_to_table(self, table_name: str, rows_to_set: Tuple, data: Tuple) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            f"insert into {table_name}{remove_quotation(rows_to_set)} values{get_amount_of_question_marks(rows_to_set)}",
            data)
        self.commit()

    def update_data_from_table(self, table_name: str, rows_to_update: Tuple, data: Tuple,
                               where: str = None):
        cursor = self.db.cursor()
        cursor.execute(
            f"update {table_name} set {add_question_mark_and_equals(rows_to_update)} {where if where is not None else ''}",
            data)
        self.commit()

    def delete_data_from_table(self, table_name: str, data: Tuple, where: str = None):
        cursor = self.db.cursor()
        cursor.execute(f"delete from {table_name} {where}", data)
        self.commit()

    def create_table(self, table_name: str, columns_names_types_and_constrains: List[Tuple[str, ...]],
                     without_row_id: bool = False):
        cursor = self.db.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} {handle_columns_names_types_and_constrains(columns_names_types_and_constrains)} {'WITHOUT ROWID' if without_row_id else ''}")
        self.commit()

    def delete_user(self, user: str):
        self.delete_data_from_table(table_name="users", where="where username=?", data=(user,))

    def commit(self):
        self.db.commit()

    def get_user(self, password: str) -> Tuple[str, str]:
        hashed_password = self.hash_password(password)
        return self.get_data_from_table(table_name="users", where="where password=?", variables=(hashed_password,),
                                        amount_to_fetch=1)

    def add_user(self, username, password: str,hashed=True):
        hashed_pass = self.hash_password(password)
        self.add_data_to_table(table_name="users", rows_to_set=("username", "password"), data=(username, hashed_pass if hashed else password))

    def create_tables(self):
        self.create_table(table_name="users", columns_names_types_and_constrains=[
            ("username", "text", "not null unique"), ("password", "text", "not null")])
        self.create_table(table_name="host", columns_names_types_and_constrains=[("domain", "text", "not null unique")])

    def get_host_rows(self) -> List[str]:
        return self.get_data_from_table("host", amount_to_fetch=0)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def get_all_users(self):
        return self.get_data_from_table("users")

    def get_password(self, username: str):
        return self.get_data_from_table("host", amount_to_fetch=1, where="where username=?", data=username)


def main():
    c = SQLClient("database.db")
    print(c.get_host_rows())
    print(c.get_all_users())


if __name__ == '__main__':
    main()
