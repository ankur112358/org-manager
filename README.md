# Organization Management

Basic system to create new organizations, and authenticate the admin users.

# How to run
We can run the service using
`docker compose up org-manager -d`

To run the test use
`docker compose up tests`

The [postman collection](./org_manager.postman_collection.json) can be used to
play around with the apis.

# DB Configurations
Sql lite is used as the database in the service. The location of the database
can be configured by using the `DATABASE_DIR` environment variable.
