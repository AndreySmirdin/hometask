SELECT Name, Rate FROM Country, LiteracyRate
WHERE Code = LiteracyRate.CountryCode
GROUP BY CountryCode
HAVING Year = max(Year)
ORDER BY Rate DESC
LIMIT 1;
