import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request



#engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    b = open("books.csv")
    reader = csv.reader(b)
    for isbn, title, author, year in reader:
    	db.execute("INSERT INTO books VALUES (:isbn, :title, :author, :year)",
    		{"isbn": isbn, "title": title, "author": author, "year": year})   
    	db.commit()

if __name__ == "__main__":
    main()
