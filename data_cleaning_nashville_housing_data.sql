SELECT
*
FROM 
	portfolio_project.nashville_housing;


    
-- Standardize SaleDate
SELECT
    SaleDate,
    DATE_FORMAT(STR_TO_DATE(SaleDate, '%M %d, %Y'), '%Y-%m-%d')
FROM
    portfolio_project.nashville_housing;
    
UPDATE 
	portfolio_project.nashville_housing
SET
	SaleDate = DATE_FORMAT(STR_TO_DATE(SaleDate, '%M %d, %Y'), '%Y-%m-%d');


    
-- Populate PropertyAddress Data
SELECT
    nash.ParcelID,
    nash.PropertyAddress AS OriginalAddress,
    subquery.NewAddress AS UpdatedAddress
FROM
    portfolio_project.nashville_housing AS nash
JOIN (
    SELECT ParcelID, MAX(PropertyAddress) AS NewAddress
    FROM portfolio_project.nashville_housing
    WHERE PropertyAddress IS NOT NULL AND PropertyAddress <> ''
    GROUP BY ParcelID
) AS subquery
ON
    nash.ParcelID = subquery.ParcelID
WHERE
    nash.PropertyAddress IS NULL OR nash.PropertyAddress = '';
    
UPDATE portfolio_project.nashville_housing
JOIN (
    SELECT nashville_housing.ParcelID, MAX(PropertyAddress) AS NewAddress
    FROM portfolio_project.nashville_housing
    WHERE PropertyAddress IS NOT NULL AND PropertyAddress <> ''
    GROUP BY ParcelID
) AS subquery
ON
    nashville_housing.ParcelID = subquery.ParcelID
SET PropertyAddress = subquery.NewAddress
WHERE
    PropertyAddress IS NULL OR PropertyAddress = '';


    
-- Breaking out Address into Individual Columns (Address, City, State)
SELECT
	PropertyAddress
FROM
	portfolio_project.nashville_housing;

SELECT
SUBSTRING(PropertyAddress, 1, INSTR(PropertyAddress, ',') - 1) as Address,
SUBSTRING(PropertyAddress, INSTR(PropertyAddress, ',') + 1, LENGTH(PropertyAddress)) as City
FROM 
	portfolio_project.nashville_housing;

-- Add two new columns
ALTER TABLE 
	portfolio_project.nashville_housing
ADD COLUMN
	PropertySplitAddress NVARCHAR(255),
ADD COLUMN    
    PropertySplitCity NVARCHAR(255);

-- Populate the new columns with respective address and city data    
UPDATE 
	portfolio_project.nashville_housing
SET
	PropertySplitAddress = SUBSTRING(PropertyAddress, 1, INSTR(PropertyAddress, ',') - 1),
	PropertySplitCity = SUBSTRING(PropertyAddress, INSTR(PropertyAddress, ',') + 1, LENGTH(PropertyAddress));
    
-- Parse OwnerAddress
SELECT
	TRIM(SUBSTRING_INDEX(OwnerAddress, ',', 1)) AS OwnerSplitAddress,
	TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(OwnerAddress, ',', -2), ',', 1)) AS OwnerSplitCity,
    TRIM(REVERSE(SUBSTRING_INDEX(REVERSE(OwnerAddress), ',', 1))) AS OwnerSplitState
FROM
	portfolio_project.nashville_housing;

-- Add three new columns for owner address
ALTER TABLE portfolio_project.nashville_housing
ADD COLUMN OwnerSplitAddress VARCHAR(255) AFTER OwnerAddress,
ADD COLUMN OwnerSplitCity VARCHAR(255) AFTER OwnerSplitAddress,
ADD COLUMN OwnerSplitState VARCHAR(2) AFTER OwnerSplitCity;
    
-- Populate the new columns with respective owner address, city, and state    
UPDATE
	portfolio_project.nashville_housing
SET
	OwnerSplitAddress = TRIM(SUBSTRING_INDEX(OwnerAddress, ',', 1)),
	OwnerSplitCity = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(OwnerAddress, ',', -2), ',', 1)),
    OwnerSplitState = TRIM(REVERSE(SUBSTRING_INDEX(REVERSE(OwnerAddress), ',', 1))); 


-- Change Y and N to Yes and No in "Sold as Vacant" field
SELECT 
	DISTINCT(SoldAsVacant), 
    COUNT(SoldAsVacant)
FROM portfolio_project.nashville_housing
GROUP BY SoldAsVacant
ORDER BY 2;

SELECT
	SoldAsVacant,
	CASE 
		WHEN SoldAsVacant = 'Y' THEN 'Yes'
		WHEN SoldAsVacant = 'N' THEN 'No'
        ELSE SoldAsVacant
    END AS SoldAsVacantDescription
FROM portfolio_project.nashville_housing;

UPDATE 
	portfolio_project.nashville_housing
SET SoldAsVacant = 
	CASE 
		WHEN SoldAsVacant = 'Y' THEN 'Yes'
		WHEN SoldAsVacant = 'N' THEN 'No'
        ELSE SoldAsVacant
	END;
    
    
-- Remove Duplicates
WITH row_num_cte as (
	SELECT
		*,
		ROW_NUMBER() OVER (PARTITION BY ParcelID, PropertyAddress, SalePrice, SaleDate, LegalReference ORDER BY UniqueID) AS row_num
	FROM
		portfolio_project.nashville_housing
)

DELETE
FROM
	row_num_cte
WHERE 
	row_num > 1;


-- Remove Unused Columns    
SELECT
	*
FROM
	portfolio_project.nashville_housing;

ALTER TABLE portfolio_project.nashville_housing
DROP COLUMN OwnerAddress,
DROP COLUMN TaxDistrict,
DROP COLUMN PropertyAddress;

