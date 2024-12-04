/*To load data from S3, I first created an external stage in Snowflake that points to S3 bucket.*/

CREATE OR REPLACE STAGE my_s3_stage
URL = 's3://your-bucket-name/path-to-your-data/'
CREDENTIALS = (AWS_KEY_ID = '<AWS_ACCESS_KEY_ID>' AWS_SECRET_KEY = '<AWS_SECRET_ACCESS_KEY>')
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

/*Once the stage is created,I loaded data into my Snowflake table */

COPY INTO airbnb_listings
FROM @my_s3_stage
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

