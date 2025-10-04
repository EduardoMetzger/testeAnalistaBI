{{ config(materialized='table') }}

select
    *
from read_csv_auto('C:/Users/eduar/OneDrive/Área de Trabalho/EduardoMetzger/testeAnalistaBI/an_bi/spreadsheets/empresas_bolsa.csv', HEADER=TRUE)
