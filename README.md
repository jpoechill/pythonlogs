# Logs Analysis

This command line app will report log information from an SQL database regarding articles and authors. It requires a terminal, SQL and Python to run. VirtualBox and Vagrant are also required as a base to run the virtual server.

To get running, please first set up views, and then run with Python.

## Set up Vagrant virtual machine

  1. Starting and running the virtual machine
    Inside the 'vagrant' directory, run `vagrant up` to download the Linux OS
    Once running, run `vagrant ssh` to login into appropriate command line

## Set up app:

  1. Import newsdata in database
    `psql -d news -f newsdata.sql`

  2. Connect to database
    `psql news`

## Create views
  1. Top Articles with Article Slug, and View Count

  ```sql
  CREATE VIEW toparticles AS
  SELECT replace(path, '/article/', '') AS slug,
  count(path) FROM log
  WHERE path != '/'
  GROUP BY log.path;
  ```

  2. Unique Articles with Author, Slug, and Read Count
  ```sql
  CREATE VIEW uniquearticles AS
  SELECT articles.author, toparticles.title, toparticles.count
  FROM toparticles, articles
  WHERE toparticles.slug = articles.slug
  ORDER BY count DESC;
  ```

  3. Total Errors Per Unique Day
  ```sql
  CREATE VIEW errsperday AS
  SELECT DISTINCT time::date AS uniqueday,
  count(*) FROM log
  WHERE status != '200 OK'
  GROUP BY uniqueday;
  ```

  4. Total Requests Per Unique Day
  ```sql
  CREATE VIEW reqsperday AS
  SELECT DISTINCT time::date AS uniqueday,
  count(*) AS totalreqs FROM log
  GROUP BY uniqueday;
  ```

  5. Total Errors/Requests Per Day
  ```sql
  CREATE VIEW errsreqsperday AS
  SELECT count AS errs,
  totalreqs AS reqs,
  errsperday.uniqueday AS day
  FROM errsperday, reqsperday
  WHERE reqsperday.uniqueday = errsperday.uniqueday;
  ```

  6. Days with percent errors
  ```sql
  CREATE VIEW daywithpercenterrors AS
  SELECT day,
  cast((cast((cast(errs AS float) / cast(reqs AS float)) AS
  decimal(10, 4)) * 100) AS
  decimal(10, 2)) AS percent
  FROM errsreqsperday;
  ```

## Run app:

  1. In Terminal (command line) run the python app by:
      `python logs.py`
