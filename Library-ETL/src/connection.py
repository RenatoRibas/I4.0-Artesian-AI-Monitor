import csv
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Constante para ajuste
CONSTANTE = 109205

def convert_to_datetime(pk_TimeStamp):
    # Converter o valor de pk_TimeStamp para "100ms day ticks"
    resultado = pk_TimeStamp / 60 / 60 / 24 / 10000000
    resultado -= CONSTANTE

   # formated_timestamp = datetime.datetime.fromtimestamp(pk_TimeStamp)

    # Convertendo para data e hora
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


csv_file_path = "dataimport.csv"

#sqlite_db_path = r"\\192.168.0.168\Historico_ML_Data\WA-HMI_RT_Eskimo_TLG9519\WA-HMI_RT_Eskimo_TLG9519_20240513_184552 - Copia (2).db3"
sqlite_db_path = r"\\192.168.0.168\Historico_ML_Data\WA-HMI_RT_Eskimo_TLG9519\WA-HMI_RT_Eskimo_TLG9519_20240513_184552.db3"
sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}")
sqlite_conn = sqlite_engine.connect()

sql_expression = text("SELECT * FROM LoggedProcessValue")
result = sqlite_conn.execute(sql_expression)

with open(csv_file_path, "w", newline="") as csv_file:
  
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(result.keys())
    

    for row in result:
        
        pk_timestamp = row.pk_TimeStamp
        pk_timestamp = convert_to_datetime(pk_timestamp) 
        row_values = list(row)
        row_values[0] = pk_timestamp  # A posição 0 é a posição da coluna pk_TimeStamp
        csv_writer.writerow(row_values)

sqlite_conn.close()

print(f"Arquivo CSV '{csv_file_path}' criado com sucesso.")
