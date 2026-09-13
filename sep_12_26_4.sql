-- 1. upload manually from file

select count(1) from  ANALYSIS_SEP_2026.SOCIAL.SOCIAL_POSTS_RAW; -- 400 

-- describe 

describe table ANALYSIS_SEP_2026.SOCIAL.SOCIAL_POSTS_RAW;
/* 
name	type	kind	null?	default	primary key	unique key	check	expression	comment	policy name	privacy domain	write default
POST_ID	NUMBER(38,0)	COLUMN	Y		N	N						
POST_TEXT	VARCHAR(16777216)	COLUMN	Y		N	N						
*/

-- sample : just two columns

select * from ANALYSIS_SEP_2026.SOCIAL.SOCIAL_POSTS_RAW limit 3;
/* 
1	Just booked a weekend trip and already started planning every meal. Maybe I'm overthinking it.
2	Today: The restaurant's soup was simple but absolutely delicious. Anyone else?
3	Honestly, Found a quiet little neighborhood that wasn't in any guidebook.
*/

-- 2. move down from SOCIAL_POSTS_RAW -> SOCIAL_POSTS using SQL
-- check rowcount in social_posts
INSERT INTO social_posts (post_id, post_text)
SELECT post_id, post_text
FROM social_posts_raw;


SELECT COUNT(*)
FROM social_posts; 

-- 4. move data from SOCIAL_POSTS -> SOCIAL_POSTS_SENTIMENT using python

-- 5. verify final target table SOCIAL_POSTS_SENTIMENT

SELECT *
FROM SOCIAL_POSTS_SENTIMENT
LIMIT 10;

SELECT SENTIMENT, COUNT(*)
FROM ANALYSIS_SEP_2026.SOCIAL.SOCIAL_POSTS_SENTIMENT
GROUP BY SENTIMENT
ORDER BY SENTIMENT;

/* 
SENTIMENT	COUNT(*)
negative	36
neutral	111
positive	253
*/
