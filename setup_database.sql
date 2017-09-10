DROP DATABASE IF EXISTS news;

CREATE DATABASE news;

\c news

\i newsdata.sql

CREATE VIEW toparticles AS
SELECT replace(path, '/article/', '') AS slug,
count(path) FROM log
WHERE path != '/'
GROUP BY log.path;

CREATE VIEW uniquearticles AS
SELECT articles.author, articles.title, toparticles.count
FROM toparticles, articles
WHERE toparticles.slug = articles.slug
ORDER BY count DESC;

CREATE VIEW errsperday AS
SELECT DISTINCT time::date AS uniqueday,
count(*) FROM log
WHERE status != '200 OK'
GROUP BY uniqueday;

CREATE VIEW reqsperday AS
SELECT DISTINCT time::date AS uniqueday,
count(*) AS totalreqs FROM log
GROUP BY uniqueday;

CREATE VIEW errsreqsperday AS
SELECT count AS errs,
totalreqs AS reqs,
errsperday.uniqueday AS day
FROM errsperday, reqsperday
WHERE reqsperday.uniqueday = errsperday.uniqueday;

CREATE VIEW daywithpercenterrors AS
SELECT day,
cast((cast((cast(errs AS float) / cast(reqs AS float)) AS
decimal(10, 4)) * 100) AS
decimal(10, 2)) AS percent
FROM errsreqsperday;
