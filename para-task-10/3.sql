SELECT Name FROM City
WHERE City.Id = (
	SELECT CityId FROM Capital
	WHERE Capital.CountryCode = (
		SELECT Code FROM Country
		WHERE Name = 'Malaysia'
	)
);
