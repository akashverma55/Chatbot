-- Movies Part --
SELECT * FROM moviesdb.movies;
select title, industry from moviesdb.movies;
select * from movies where industry="Bollywood";
select count(*) from movies where industry="Bollywood";
SELECT distinct industry FROM movies;
select * from movies where title like "%THOR%";
select * from movies where title like "%america%";
select * from movies where studio="";
select * from movies where imdb_rating is null;
select * from movies where imdb_rating>=9;
select * from movies where imdb_rating>=6 and imdb_rating<=8;
select * from movies where imdb_rating between 6 and 8;
select * from movies where release_year=2019 or release_year=2018;
select * from movies where release_year in (2018,2019);
select * from movies where studio in ("marvel studios","Zee studios");
select * from movies where industry="bollywood" order by imdb_rating desc limit 5 offset 3;


select round(avg(imdb_rating),2) as avg_rating,
max(imdb_rating) as max_rating,
min(imdb_rating) as min_rating
from movies where studio="Marvel studios";

select industry, count(*) from movies group by industry;
select studio, count(*) as cnt from movies group by studio order by cnt desc;
select industry, count(industry) as cnt,
round(avg(imdb_rating),2) as avg from movies group by industry;
select studio, count(studio) as cnt,
round(avg(imdb_rating),2) as avg from movies group by studio order by avg desc;
select studio, count(studio) as cnt,
round(avg(imdb_rating),2) as avg from movies where studio!="" group by studio order by avg desc;

-- SELECT--> FROM--> WHERE--> GROUP BY--> HAVING--> ORDER BY --
select release_year, count(*) as movie_count from movies group by release_year
having movie_count>2 order by movie_count desc;


-- Actors Part --
SELECT * FROM moviesdb.actors;
select year(curdate()) as current_year;


-- Financial Part --
select * from financials;
select *, (revenue-budget) as profit from financials;
select *,if (currency="USD", revenue*80, revenue) as revenue_inr from financials;
select distinct unit from financials;
select *,
	case
		when unit="thousands" then revenue/1000
        when unit="billions" then revenue*1000
        else revenue
	end as revenue_inr 
from financials;


-- join --

-- this join will join both movies and financial but remove the data that are empty and by default its inner join-- 
select m.movie_id, title, budget, revenue, currency, unit from movies m
join financials f on m.movie_id=f.movie_id;

-- left join means from table and add the column of join table mentioned in select even if its empty --  
select m.movie_id, title, budget, revenue, currency, unit from movies m
left join financials f on m.movie_id=f.movie_id;

-- right join means join table and add the column of from table mentioned in select even if its empty --  
select f.movie_id, title, budget, revenue, currency, unit from movies m
right join financials f on m.movie_id=f.movie_id;

-- both left and right join we use union -- 
select m.movie_id, title, budget, revenue, currency, unit from movies m
left join financials f on m.movie_id=f.movie_id
UNION
select f.movie_id, title, budget, revenue, currency, unit from movies m
right join financials f on m.movie_id=f.movie_id;

select movie_id, title, budget, revenue, currency, unit from movies m
right join financials f using (movie_id);