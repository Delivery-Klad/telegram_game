import psycopg2


def connect():
    try:
        con = psycopg2.connect(
            host="ec2-52-20-248-222.compute-1.amazonaws.com",
            database="d36btqimpd50q8",
            user="jtkildzdefkqjn",
            port="5432",
            password="75f3f173d48f189115d619cd2185561b70cb7c41696c76c1dd5036b123000e88")

        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
