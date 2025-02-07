# **Weather Data Pipeline with Apache Airflow**

## **Project Overview**
- This project is an automated data pipeline that extracts, transforms, and uploads weather data for Luxor to an Amazon S3 bucket.
- Built using Apache Airflow, the pipeline fetches real-time weather data from the OpenWeather API.

---

## **Key Features**
1. **Automated Workflow**: The pipeline automates the process of fetching and storing weather data daily.
2. **Data Transformation**: Converts raw API data into a structured, human-readable CSV format.
3. **Cloud Storage**: Stores the processed weather data in an Amazon S3 bucket for long-term storage or analysis.
4. **Scalability**: Easily extendable to handle data for multiple cities or additional weather parameters.

---

## **Technologies Used**
- **Apache Airflow**: Orchestrates the pipeline tasks.
- **OpenWeather API**: Provides real-time weather data.
- **Amazon S3**: Cloud storage for processed data.
- **Python Libraries**: 
  - `pandas` for data transformation.
  - `json` for parsing API responses.
- **Docker**: Used for running Airflow in a containerized environment.

---

## **Pipeline Workflow**
1. **Check Weather Data Availability**: Ensures the API is accessible.
2. **Extract Weather Data**: Fetches weather data for Luxor from OpenWeather API.
3. **Transform Weather Data**: Processes and formats the data into a CSV file.
4. **Upload to S3**: Uploads the CSV file to a specified S3 bucket.

---

## **Setup and Installation**
1. **Prerequisites**:
   - Docker and Docker Compose.
   - AWS S3 Bucket and IAM credentials.
   - OpenWeather API key.
2. **Steps**:
   - Clone the repository.
   - Configure `.env` file with:
     - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for S3.
     - `OPENWEATHER_API_KEY` for API access.
   - Start the Airflow containers with `docker-compose up`.
   - Access the Airflow web UI at `http://localhost:8080`.

---

## **Configuration**
- The pipeline uses the following connections:
  - `openweather_api`: HTTP connection for the OpenWeather API.
  - `s3_conn`: AWS connection for uploading data to S3.

---

## **How to Run the Pipeline**
1. Start the Airflow scheduler and web server:
   ```bash
   docker-compose up
   
2. Trigger the pipeline manually or let it run on its daily schedule.

---

## **Output**
- The pipeline generates a CSV file with the weather data for Luxor.
- The file is stored in the S3 bucket with a timestamped filename.
