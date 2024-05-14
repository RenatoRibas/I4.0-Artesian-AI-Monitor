from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

CONSTANTE = 109205

# Função para converter timestamp Unicode em datetime
def convert_to_datetime(pk_TimeStamp):
    resultado = float(pk_TimeStamp) / 60 / 60 / 24 / 10000000
    resultado -= CONSTANTE

    data_base = datetime(1899, 12, 31)
    dias = int(resultado)
    parte_decimal = resultado - dias

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
    sqlite_db_path = r"\\192.168.0.168\Historico_ML_Data\WA-HMI_RT_Eskimo_TLG9519\WA-HMI_RT_Eskimo_TLG9519_20240513_184552 - Copia.db3"
    sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}")
    sqlite_conn = sqlite_engine.connect()
    sql_expression = text("SELECT * FROM LoggedProcessValue")
    result = sqlite_conn.execute(sql_expression)
    sqlite_conn.close()

    postgresql_engine = create_engine('postgresql://postgres:postgres@localhost:5432/DW_Server')

    for row in result:
        id_motor = 1
        status = True  
        spFrequencia = 60.0
        feedCorrente = row[3]
        feedTensaoEntrada = 380.0
        timestamp = convert_to_datetime(row[0])

        upsert_query = text(f"""
        INSERT INTO public.datalogmotores (id_motor, status, spFrequencia, feedCorrente, feedTensaoEntrada, timestamp)
        VALUES (:id_motor, :status, :spFrequencia, :feedCorrente, :feedTensaoEntrada, :timestamp)
        ON CONFLICT (timestamp) DO NOTHING;
        """)
        
        with postgresql_engine.connect() as conn:
            conn.execute(upsert_query, id_motor=id_motor, status=status, spFrequencia=spFrequencia,
                         feedCorrente=feedCorrente, feedTensaoEntrada=feedTensaoEntrada, timestamp=timestamp)

    print("Dados inseridos na tabela DatalogMotores com sucesso.")

def main():
    insert_data_into_postgresql()

if __name__ == "__main__":
    main()
