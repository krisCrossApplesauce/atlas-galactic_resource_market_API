from flask import Flask, jsonify
import psycopg2

conn = psycopg2.connect(
    dbname="galactic_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
