#!/bin/bash

# Variables (Change the password if needed)
DB_NAME="kikapu_kash_db"
DB_USER="kikapu_admin"
DB_PASS="Admin@1234"

# Switch to postgres user and run commands
sudo -u postgres psql <<EOF
-- Create Database
CREATE DATABASE $DB_NAME;

-- Create User
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';

-- Grant Privileges
ALTER DATABASE $DB_NAME OWNER TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Exit
\q
EOF

echo "✅ PostgreSQL database '$DB_NAME' and user '$DB_USER' have been created successfully!"
