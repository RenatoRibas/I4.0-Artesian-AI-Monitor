from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

# Constante para ajuste

CONSTANTE = 109205

def convert_to_datetime(pk_TimeStamp):

    # Converter o valor de pk_TimeStamp para "100ms day ticks"
    resultado = pk_TimeStamp / 60 / 60 / 24 / 10000000
    resultado -= CONSTANTE #resultado em ponto flutuante

    # Convertendo para data e hora
    data_base = datetime(1899, 12, 31)
    
    dias = int(resultado)
    parte_decimal = resultado - dias #ponto flutuante

    data = data_base + timedelta(days=dias)

    horas = int(parte_decimal * 24)
    parte_decimal -= horas / 24
    minutos = int(parte_decimal * 60)
    parte_decimal -= minutos / 60
    segundos = int(parte_decimal * 60)
    parte_decimal -= segundos / 60
    microssegundos = int(parte_decimal * 1000000)

    return data + timedelta(hours=horas, minutes=minutos, seconds=segundos, microseconds=microssegundos)

def insert_data_into_postgresql():
    conn = psycopg2.connect(
        dbname="DW_Server",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Conexão com o banco de dados SQLite
    sqlite_db_path = r"\\192.168.0.168\Historico_Bombas_Pocos\WA-HMI_RT_Eskimo_TLG2443_20240422_192501.db3"
    sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}")

    # Criar uma conexão com o SQLite
    sqlite_conn = sqlite_engine.connect()

    # Criar um objeto de expressão SQL para a consulta no SQLite
    sql_expression = text("SELECT * FROM LoggedProcessValue")

    # Executar a consulta no SQLite
    result = sqlite_conn.execute(sql_expression)

    # Fechar a conexão com o SQLite
    sqlite_conn.close()

    # Query SQL para realizar a operação de MERGE no PostgreSQL
    merge_query = f"""
    WITH LoggedProcessValue_relacional AS (
           SELECT pk_TimeStamp, pk_fk_Id, Value
           FROM LoggedProcessValue
        )
        MERGE INTO
        public.datalogmotores AS d
        USING
            LoggedProcessValue_relacional  AS r
        ON r.pk_TimeStamp = d.timestamp 
        WHEN NOT MATCHED THEN
            INSERT (id_motor, status, spFrequencia, feedCorrente, feedTensaoEntrada, timestamp)
            VALUES (1, 1, 60.0, r.Value, 380.0, r.pk_TimeStamp);
    """

    cursor.execute(merge_query)
    conn.commit()
    conn.close()

    print("Dados inseridos na tabela DatalogMotores com sucesso.")

def main():
    insert_data_into_postgresql()

if __name__ == "__main__":
    main()

