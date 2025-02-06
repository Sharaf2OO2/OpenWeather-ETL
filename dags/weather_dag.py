from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
import json

default_args = {
    'owner': 'Sharaf',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG('weather_dag',
            default_args=default_args,
            description='A simple weather DAG',
            schedule_interval='@daily',
            catchup=False) as dag:
            
            is_weather_available = HttpSensor(
                    task_id='is_weather_available',
                    http_conn_id='openweather_api',
                    endpoint='/data/2.5/weather?q=Luxor&appid=36907b823b85ecf2a3bf5630d2be0284'
                    )