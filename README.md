# data_pipeline-airflow-pyspark
This project is a batch process data pipeline utilized with the PySpark

## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Workflow](#workflow)

## Introduction
This project is a batch process data pipeline utilized with the PySpark artifact above. As soon as data lands on the AWS S3 bucket, that triggers airflow and causes the PySpark downstream operation which converts the CSV file on the S3 bucket into a parquet file. After that, the parquet is used in AWS Athena as a data set. Finally, Superset can visualize the data using the data set.

![DIAGRAM](https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/diagram_project1.png)
	
## Technologies
Project is created with:
* Spark Version = 3.1.2
* Hadoop Version = 3.2
* Python Version = 3.8
* Docker Compose = 1.29.1
* Airflow Version = 2.1.0
* Superset = [apache/superset - Docker Image | Docker Hub](https://hub.docker.com/r/apache/superset)
	
## Workflow
1. Set up Docker environment with airflow in EC2. And install the Docker compose and Airflow following guides.
- [Docker basics for Amazon ECS - Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
- [Install Docker Compose | Docker Documentation](https://docs.docker.com/compose/install/)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

2. Save data in S3 bucket with CSV format. (If change the file option in the artifact, we can use other data formats like txt, parquet too.)
In my case, extracted data as CSV from Stack Overflow by [my web scraper](https://github.com/ChloeHeekSuh/SO_Web_Scraper)

3. When data is landing on the S3 bucket, airflow is triggered to make the downstream work. A lambda function acts as the trigger.
Lambda Function determines which airflow dag this data should be forwarded to when an event is triggered. Then, Airflow starts to find key information. Key information will be including file path, table name, database name, etc. We can check the working infomaition in AWS Cloud Watch.
<img src="https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/lambda_project1.png" width="700">
<img src="https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/cloudwatch_project_1.png" width="900">

5. Once the spark job is submitted to the worker node, airflow knows where the EMR cluster is located and starts to hand over jobs to the EMR cluster.

6. Then EMR cluster starts to transform the CSV to parquet using the PySpark artifact that we saved in S3. It says to the EMR cluster, "Hey, we have a file and it's transformed to Parquet file, and register with Glue catalog, so the end-user can use the data."
To explain more, The zip file above serves as an engine. This artifact delivers to the EMR cluster as follows. "That's going to your artifact that going to be a blueprint transforming the incoming data." Then, it is divided into partitions designated by us and stored as a Parquet file in S3 bucket.

7. Set up a crawler and scan the data and automatically populate the Glue catalog. Then we can use it as a schema in AWS Athena.
<img src="https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/glue_project_1.png" width="1000">
<img src="https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/athena_project_1.png" width="1000">

8. For data visualization, import the schema to a Superset. The superset is a UI portal for visualizing and viewing data into charts, tables, etc. 
<img src="https://github.com/ChloeHeekSuh/data_pipeline-airflow-pyspark/blob/master/screenshot_batch/superset_project_1.png" width="1000">
