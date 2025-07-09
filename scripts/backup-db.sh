#!/bin/bash

# === CONFIGURATION ===
DB_NAME="invoiceplanepy"         # Change to your database name
DB_USER="postgres"               # Change to your DB user
BACKUP_DIR="./backups"           # Where to store backups
GPG_RECIPIENT="your@email.com"   # GPG key or email to encrypt for

# === SCRIPT ===
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
ENCRYPTED_FILE="$BACKUP_FILE.gpg"

mkdir -p "$BACKUP_DIR"

echo "Creating database dump..."
pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

if [ $? -ne 0 ]; then
    echo "Database dump failed!"
    rm -f "$BACKUP_FILE"
    exit 1
fi

# Fetch the GPG public key from Ubuntu keyserver if not already present
echo "Ensuring GPG public key for $GPG_RECIPIENT is available..."
gpg --list-keys "$GPG_RECIPIENT" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Fetching public key for $GPG_RECIPIENT from keyserver..."
    gpg --keyserver keyserver.ubuntu.com --recv-keys "$GPG_RECIPIENT" || {
        echo "Failed to fetch GPG key for $GPG_RECIPIENT"
        rm -f "$BACKUP_FILE"
        exit 3
    }
fi

echo "Encrypting backup with GPG..."
gpg --yes --output "$ENCRYPTED_FILE" --encrypt --recipient "$GPG_RECIPIENT" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Encrypted backup created at $ENCRYPTED_FILE"
    rm -f "$BACKUP_FILE"
else
    echo "GPG encryption failed!"
    rm -f "$BACKUP_FILE"
    exit 2
fi