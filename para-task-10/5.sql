SELECT  GovernmentForm, SUM(SurfaceArea) AS SumArea
FROM Country
GROUP BY GovernmentForm
ORDER BY SumArea DESC
LIMIT 1;
