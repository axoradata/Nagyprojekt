import psycopg2

import datetime
import random
import string


class Token:
    now = datetime.datetime.now()

    def create_token(self) -> str:
        token: str = ""

        token += self.create_token_header()
        token += self.create_token_body()

        # max length of token 64
        generated_str = 64 - len(token)

        token += self.create_token_footer(generated_str)

        token_list = list(token)
        random.shuffle(token_list)
        return ''.join(token_list)

    def validator(self, token, disposition:tuple) -> bool:
        user = self.get_token(token)

        if user != 'False':
            user_disposition = self.get_disposition(user)
            if user_disposition != 'False':
                if user_disposition in disposition: return True
                else: return False
            else: return False
        else: return False

    def create_token_header(self) -> str:
        token_header = ''

        year = self.now.year
        month = self.now.month
        day = self.now.day

        token_header += str(hex(year))
        token_header += str(hex(month))
        token_header += str(hex(day))

        return token_header
    def create_token_body(self) -> str:
        token_body = ''

        hour = self.now.hour
        minute = self.now.minute
        second = self.now.second
        microsecond = self.now.microsecond

        token_body += str(hex(hour))
        token_body += str(hex(minute))
        token_body += str(hex(second))
        token_body += str(hex(microsecond))

        return token_body
    @staticmethod
    def create_token_footer(length: int) -> str:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_string

    def get_token(self, token: str) -> str:
        card_id = None

        conn = psycopg2.connect(
            host="localhost",
            dbname="elephant",
            user="postgres",
            password="1234567",
            port=5432)

        cur = conn.cursor()

        try:
            cur.execute(f"""
                SELECT card_id FROM users WHERE token = '{token}';
            """)
            card_id = cur.fetchone()
            conn.commit()
        except Exception as e:
            print("Database error in 'get token' branch because:")
            print(e)
        finally:
            cur.close()
            conn.close()
            if card_id:
                return card_id[0]
            else:
                return 'False'

    def get_disposition(self, card_id: str) -> str:
        disposition = ''

        conn = psycopg2.connect(
            host="localhost",
            dbname="elephant",
            user="postgres",
            password="1234567",
            port=5432)

        cur = conn.cursor()

        try:
            cur.execute(f"""
                SELECT disposition FROM employee WHERE card_id = '{card_id}';
            """)
            disposition = cur.fetchone()
            conn.commit()
        except Exception as e:
            print("Database error in 'insert into' branch because:")
            print(e)
        finally:
            cur.close()
            conn.close()
            if card_id:
                return disposition[0]
            else:
                return 'False'


#test = Token()
#print(test.create_token())