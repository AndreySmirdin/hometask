SELECT Country.Name, COUNT(*) AS CityCnt FROM Country
JOIN City ON Country.Code = City.CountryCode WHERE City.Population > 1000000
GROUP BY Country.Code
ORDER BY CityCnt DESC;
