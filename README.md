# FastAPI_Redis_MongoDB_Caching_Example

![Tests](https://github.com/wojciechignasiak/FastAPI_Redis_MongoDB_Caching_Example/actions/workflows/push.yml/badge.svg?event=push)

This repository is a guide on how to implement data caching using the Write-Through technique, utilizing FastAPI, Redis, and MongoDB. It demonstrates how to apply the Write-Through caching technique in a FastAPI application to enhance application performance and scalability.

<br>
<p align="center">
<img src="images/diagram.png" alt="Project diagram"/>
</p>
<br>

## Technologies

* FastAPI
* Redis
* MongoDB

## Running

Assuming you already have Docker and docker-compose installed, execute the following command in the root directory of the project:

`docker-compose up -d`

This should install all dependencies, configure, and run the FastAPI, Redis, and MongoDB containers.

## Example Usage

Upon running, you can see the interactive FastAPI documentation by navigating to http://localhost:8081/fastapi-app/docs

## Example endpoints:
* $${\color{green}POST}$$ **/fastapi-app/create-software-developer**: add a new item.
* $${\color{blue}GET}$$ **/fastapi-app/get-software-developer**: fetch item details.
* $${\color{orange}PATCH}$$ **/fastapi-app/update-software-developer**: update item.
* $${\color{red}DELETE}$$ **/fastapi-app/delete-software-developer**: delete item.


## Description of Write-Through Caching Technique

The Write-Through caching technique involves writing data to both the cache and the primary database simultaneously. When the application writes new data, this data is written to Redis (cache) and MongoDB (primary database) at the same time.

This ensures data consistency between the cache and the primary database and enables fast data reading from the cache, significantly improving application performance.
