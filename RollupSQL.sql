
SELECT 
    CASE WHEN category IS NULL THEN 'AllCategories' ELSE category end AS Category,
    CASE WHEN company IS NULL THEN 'Total' ELSE company end AS Company,
    TotalCount
FROM
    (SELECT category, company, count(*) as TotalCount  FROM NewsStoriesProduction GROUP BY category, company with rollup) RLP