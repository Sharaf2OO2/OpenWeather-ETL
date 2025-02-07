from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
import json, pandas as pd

default_args = {
    'owner': 'Sharaf',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def upload_to_s3(task_instance):
    s3_hook = S3Hook(aws_conn_id='s3_conn')
    dt_string = task_instance.xcom_pull(key='timestamp')
    local_file = f'Current_Weather_Data_Luxor_{dt_string}.csv'
    s3_bucket = 'luxor-weather-data'
    s3_key = f'{local_file}'
    s3_hook.load_file(filename=local_file, key=s3_key, bucket_name=s3_bucket, replace=True)

def kelvin_to_fahrenheit(kelvin_temp):
    return round((kelvin_temp - 273.15) * 9/5 + 32, 2)

def transform_loaded_data(task_instance):
    data = task_instance.xcom_pull(task_ids='extract_weather_data')
    city = data['name']
    weather_description = data['weather'][-1]['description']
    temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp'])
    feels_like_fahrenheit = kelvin_to_fahrenheit(data['main']['feels_like'])
    min_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_min'])
    max_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {
                'City': city,
                'Description': weather_description,
                'Temprature (F)': temp_fahrenheit,
                'Feels Like (F)': feels_like_fahrenheit,
                'Minimum Temprature (F)': min_temp_fahrenheit,
                'Maximum Temprature (F)': max_temp_fahrenheit,
                'Pressure': pressure,
                'Humidity': humidity,
                'Wind Speed': wind_speed,
                'Time of Record': time_of_record,
                'Sunrise (Local Time)': sunrise_time,
                'Sunset (Local Time)': sunset_time
    }

    df_data = pd.DataFrame([transformed_data])

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    task_instance.xcom_push(key='timestamp', value=dt_string)
    dt_string = f'Current_Weather_Data_Luxor_{dt_string}'
    df_data.to_csv(f'{dt_string}.csv', index=False)

with DAG('weather_dag',
            default_args=default_args,
            description='A simple weather DAG',
            schedule_interval='@daily',
            catchup=False) as dag:
            
            is_weather_available = HttpSensor(
                    task_id='is_weather_available',
                    http_conn_id='openweather_api',
                    endpoint='/data/2.5/weather?q=Luxor&appid=5add628cbaf526e01cd7d8610492317b'
                    )
            
            extract_weather_data = SimpleHttpOperator(
                    task_id='extract_weather_data',
                    http_conn_id='openweather_api',
                    method='GET',
                    endpoint='/data/2.5/weather?q=Luxor&appid=5add628cbaf526e01cd7d8610492317b',
                    response_filter=lambda response: json.loads(response.text),
                    log_response=True
                    )

            transform_weather_data = PythonOperator(
                    task_id='transform_weather_data',
                    python_callable=transform_loaded_data
                    )
            
            upload_to_s3 = PythonOperator(
                    task_id='upload_to_s3',
                    python_callable=upload_to_s3
                    )

            is_weather_available >> extract_weather_data >> transform_weather_data >> upload_to_s3
