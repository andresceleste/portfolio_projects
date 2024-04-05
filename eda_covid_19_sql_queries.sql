SELECT 
	*
FROM 
	portfolio_project.covid_deaths
WHERE 
	continent IS NOT NULL
ORDER BY 
	3, 4;

SELECT 
	*
FROM 
	portfolio_project.covid_vaccinations
ORDER BY 
	3, 4;

-- Select data we will be going to use

SELECT 
	location, 
    date, 
    total_cases, 
    new_cases, 
    total_deaths, 
    population
FROM 
	portfolio_project.covid_deaths
ORDER BY 
	1, 2;

-- Total Cases vs Total Deaths
SELECT 
	location, 
    date, 
    total_cases, 
    total_deaths, 
    (total_deaths/total_cases)*100 AS death_percentage
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
ORDER BY 
	1, 2;

-- Total Cases vs Population
SELECT 
	location, 
    date, 
    population, 
    total_cases, 
    (total_cases/population)*100 AS percent_population_infected
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
ORDER BY 
	1, 2;

-- Countries with highest infection rate compared to population
SELECT 
	location, 
    population, 
    MAX(total_cases) AS highest_infection_count, 
    MAX((total_cases/population))*100 AS percent_population_infected
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
GROUP BY 
	location, population    
ORDER BY 
	percent_population_infected DESC;

-- Total death count by location (country)
SELECT 
	location, 
    MAX(total_deaths) AS total_death_count
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
GROUP BY 
	location
ORDER BY 
	total_death_count DESC;

-- Continents with the highest death count per population
SELECT 
	continent, 
    MAX(total_deaths) AS total_death_count
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
GROUP BY 
	continent
ORDER BY 
	total_death_count DESC;

-- Global Numbers
SELECT 
	date, 
    SUM(new_cases) AS total_cases, 
    SUM(new_deaths) AS total_deaths, 
    SUM(new_deaths)/SUM(new_cases)*100 AS death_percentage
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
GROUP BY 
	date
ORDER BY 
	1, 2;

-- Global Numbers: Total Deaths
SELECT 
	SUM(new_cases) AS total_cases, 
    SUM(new_deaths) AS total_deaths, 
    SUM(new_deaths)/SUM(new_cases)*100 AS death_percentage
FROM 
	portfolio_project.covid_deaths
WHERE 
	total_deaths IS NOT NULL
	AND continent IS NOT NULL
ORDER BY 
	1, 2;	

-- Total Population vs Vaccinations
SELECT 
	dea.continent, 
    dea.location, 
    dea.date, 
    dea.population, 
    vac.new_vaccinations, 
	SUM(CAST(new_vaccinations AS UNSIGNED)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS rolling_people_vaccinated
FROM 
	portfolio_project.covid_deaths AS dea
JOIN 
	portfolio_project.covid_vaccinations AS vac 
ON 
	dea.location = vac.location
	AND dea.date = vac.date
WHERE 
	dea.continent IS NOT NULL
	AND new_vaccinations != ''
ORDER BY 2, 3;

-- Use CTE
WITH pop_vs_vac (continent, location, date, population, new_vaccinations, rolling_people_vaccinated) AS (
    SELECT
        dea.continent,
        dea.location,
        dea.date,
        dea.population,
        vac.new_vaccinations, 
        SUM(CAST(vac.new_vaccinations AS UNSIGNED)) OVER (PARTITION BY dea.location ORDER BY dea.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_people_vaccinated
    FROM
        portfolio_project.covid_deaths AS dea
    JOIN
        portfolio_project.covid_vaccinations AS vac 
    ON
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE
        dea.continent IS NOT NULL
        AND vac.new_vaccinations != ''
)
SELECT
    *,
    (rolling_people_vaccinated/population)*100
FROM
    pop_vs_vac
ORDER BY
    location, date;

-- Temp Table
DROP TABLE IF EXISTS portfolio_project.percent_population_vaccinated;

CREATE TEMPORARY TABLE portfolio_project.percent_population_vaccinated (
	continent NVARCHAR(255),
	location NVARCHAR(255),
	DATE DATETIME,
	population numeric,
	new_vaccinations numeric,
	rolling_people_vaccinated numeric
);

INSERT INTO portfolio_project.percent_population_vaccinated (
	SELECT
        dea.continent,
        dea.location,
        dea.date,
        dea.population,
        vac.new_vaccinations, 
        SUM(CAST(vac.new_vaccinations AS UNSIGNED)) OVER (PARTITION BY dea.location ORDER BY dea.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_people_vaccinated
    FROM
        portfolio_project.covid_deaths AS dea
    JOIN
        portfolio_project.covid_vaccinations AS vac 
    ON
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE
        dea.continent IS NOT NULL
        AND vac.new_vaccinations != ''
);

SELECT
    *,
    (rolling_people_vaccinated/population)*100
FROM
    portfolio_project.percent_population_vaccinated
ORDER BY
    location, date;

-- Creating View to store data for later visualizations
CREATE VIEW portfolio_project.percent_population_vaccinated AS (
	SELECT
        dea.continent,
        dea.location,
        dea.date,
        dea.population,
        vac.new_vaccinations, 
        SUM(CAST(vac.new_vaccinations AS UNSIGNED)) OVER (PARTITION BY dea.location ORDER BY dea.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_people_vaccinated
    FROM
        portfolio_project.covid_deaths AS dea
    JOIN
        portfolio_project.covid_vaccinations AS vac 
    ON
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE
        dea.continent IS NOT NULL
        AND vac.new_vaccinations != ''
);
