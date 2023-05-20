# build base Docker image with PostgreSQL
FROM postgres:latest 

# set default PostgreSQL environment variables and set conda environment variables
ENV POSTGRES_USER db_user
ENV POSTGRES_PASSWORD LetMeIn
ENV POSTGRES_DB shot_db

# set the working directory 
WORKDIR /docker-entrypoint-initdb.d 

# copy csv files and seeding script
COPY ./data /docker-entrypoint-initdb.d/data 
COPY ./seed-database.sh /docker-entrypoint-initdb.d/seed-database.sh 
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql  

# change script permissions of the script to be executable 
RUN chmod +x /docker-entrypoint-initdb.d/seed-database.sh 