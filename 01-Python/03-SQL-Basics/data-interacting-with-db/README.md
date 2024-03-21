## Background & Objectives

The goal of this challenge is to explore an [SQLite](http://en.wikipedia.org/wiki/SQLite) database to understand its schema.

## Tool

Download and install [DBeaver](https://dbeaver.io/), a free, open-source, and powerful tool to connect to any database, explore its schema, and even **run SQL queries**.

## Data

The data for SQL challenges is stored online and can be accessed through a URL.

In each SQL challenge, you will find an empty directory named `data`.

As a good practice, all data files (`.csv`, `.sqlite`, etc.) should be stored in these folders.

Your first task is to download the databases so that you can work with them locally.

As a reminder from Data Sourcing (yesterday), here are two ways of doing so:

Through the web browser (*vanilla way*):
1. Open your web browser
2. Navigate to the URL provided
3. When prompted to, choose to save the file on your computer
4. If needed, find the file and move/copy it into the challenge's `data` directory

Through the CLI (*hacker way*):
1. Open your Terminal
2. `curl <URL> > <target-path>`

### Movies Database

We will work with the `movies.sqlite` database, available at this URL:
`https://wagon-public-datasets.s3.amazonaws.com/sql_databases/movies.sqlite`

In your Terminal, copy/paste and execute the `curl` command below to download the database into the `data` directory of this challenge.
```bash
curl https://wagon-public-datasets.s3.amazonaws.com/sql_databases/movies.sqlite \
> ~/code/<user.github_nickname>/{{local_path_to("01-Python/03-SQL-Basics/03-Interacting-with-db")}}/data/movies.sqlite
```

<details>
  <summary markdown='span'>
    <strong>⚠️ For Windows/WSL2 Users</strong>
    <span class="icon"> ⚠️ 👈 (Click me!)</span>
  </summary>

  DBeaver is installed on Windows and by default does not have enough rights to access files in your Ubuntu file system.

  As a workaround for this, please download the file **directly on Windows** rather than saving it within the Ubuntu file structure first and copying it over after. This will ensure that DBeaver can access and open the file!

  ---
</details>
<br>

## Specs

### Database schema

Open DBeaver and connect to the `data/movies.sqlite` database, then explore the different tables to answer the following questions:

- What are the tables and the relationships between tables?
- What are the columns and their types?

Use [db.lewagon.com](http://db.lewagon.com/) to draw this database's schema.

To check your solution, just click on "Save/Load", then "Save XML". Now copy/paste the generated XML code into the `movies.xml` file. You can then `make` to check your solution.

### Run SQL queries

Open a new SQL editor and run some SQL queries to answer the following question: **how many rows does each table contain?**
