# build base Docker image with PostgreSQL
FROM postgres:latest 

# set default PostgreSQL environment variables and set conda environment variables
ENV POSTGRES_USER db_user
ENV POSTGRES_PASSWORD LetMeIn
ENV POSTGRES_DB shot_db

# set the working directory 
WORKDIR /docker-entrypoint-initdb.d 

# copy csv files and seeding script
COPY ./data /data
COPY ./seed-database.sh ./seed-database.sh 
COPY ./init.sql ./init.sql  