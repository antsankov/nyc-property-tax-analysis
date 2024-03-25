# SIPA EMPA Quant Final Project

### NYC City Data
* From https://data.cityofnewyork.us/City-Government/Property-Valuation-and-Assessment-Data/yjxr-fw8i/data
* Filters: 
	- BORO is 3, 
	- TAXCLASS does not contain 3, 
	- TAXCLASS does not contain 4, 
	- POSTCODE is not blank, 
	- YEAR is 2010/11 (2012/13, 2013/14,2014/15,2015/16,2016/17,2017/18,2018/19)

### Streeteasy Data
* https://cdn-charts.streeteasy.com/sales/All/medianSalesPrice_All.zip
* https://streeteasy.com/blog/data-dashboard/

### NYC City Data Explainer

* https://www.nyc.gov/site/finance/property/definitions-of-property-assessment-terms.page - 
	Property in NYC is divided into 4 classes:

	Class 1: Most residential property of up to three units (family homes and small stores or offices with one or two apartments attached), and most condominiums that are not more than three stories.
	Class 2: All other property that is not in Class 1 and is primarily residential (rentals, cooperatives and condominiums). Class 2 includes:
	Sub-Class 2a  (4 -  6 unit rental building);
	Sub-Class 2b  (7 - 10 unit rental building);
	Sub-Class 2c  (2 - 10 unit cooperative or condominium); and
	Class 2  (11 units or more).
	Class 3: Most utility property.
	Class 4: All commercial and industrial properties, such as office, retail, factory buildings and all other properties not included in tax classes 1, 2 or 3.

BBLE (Borough, Block, and Lot): A unique identifier for properties in NYC, combining the borough code (1 digit), block number, and lot number. In your example, bble1000163859 represents a specific property in Manhattan (borough code 1).

Boro: The borough in which the property is located. 1 stands for Manhattan.

Block: A specific area within a borough defined by the city's planning department. 16 is the block number for your property.

Lot: A specific parcel of land within a block. 3859 is the lot number.

Easement: A right to use another person's property for a specified purpose. If this field is empty, it means there are no recorded easements on the property.

Owner: The name of the property owner. For your example, it's CHEN, QI TOM.

Bldgcl (Building Class): A code representing the type of building on the lot. R4 indicates a condominium.

Taxclass: The tax classification. 2 indicates it's a property other than a one-, two-, or three-family home, which typically includes buildings with more than three units, such as condos and co-ops.

Ltfront (Lot Frontage): The width of the front of the lot in feet. 0 indicates that this data may not have been entered or is not applicable.

Ltdepth (Lot Depth): The depth of the lot in feet. 0 again indicates a lack of data or not applicable.

Ext: Indicates if there is an extension on the building. If empty, it means there is no extension.

Stories: The number of floors in the building. 31 indicates a high-rise building.

Fullval (Full Market Value): The property's market value as determined by the city. $354,180 in your example.

Avland (Actual Land Value): The assessed value of the land. $3,310 initially, but then listed again as $23,310, which may indicate a revision or correction.

Avtot (Actual Total Value): The total assessed value of the property, including both land and buildings. Initially $159,381, with a revision to $2,148,953.

Exland (Exempt Land Value): The value of the land that is exempt from taxes. $3,310 initially, and then $23,310 in a revised entry.

Extot (Exempt Total Value): The total value of the property that is exempt from taxes. Initially $159,381, with a revision or correction to $148,953.

Excd (Exemption Code): A code indicating the type of tax exemption applied to the property. 16800 could correspond to a specific exemption type, such as for veterans or non-profits.

Staddr (Street Address): The street address of the property. 1 RIVER TERRACE in your example.

Zip: The ZIP code for the property. If empty, it was not provided.

Exmptcl (Exempt Class): If the property has an exemption, this code indicates the type of exemption.

Bldfront (Building Frontage): The width of the front of the building in feet. 0 indicates no data or not applicable.

Blddepth (Building Depth): The depth of the building in feet. 0 indicates no data or not applicable.

Period: The period for which the assessment is valid. FINAL indicates the final assessment for the fiscal year.

Year: The fiscal year for which the data is relevant. 2018/19 in your example.

Valtype (Valuation Type): Indicates the type of valuation. AC-TR stands for "Actual Transitional," a method of property valuation used for tax purposes.
