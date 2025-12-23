# REAL-ESTATE-SCRAPING
This project extracts the data from real estate websites which will help the client to make cold calls and have better opportunities to make his sales.


### Project Brief: Distressed Property Scraper

**Client Request**

> "I need a list of 'stale' listings on Redfin or Realtor.com that aren't moving. I only want motivated sellers."

**Target Market**

* **Location:** Atlanta, GA
* **Zip Codes:** 30310, 30311, 30314
* **Property Type:** Single Family Homes

**Filtering Criteria (The "Deal" Logic)**

1. **Days on Market:** Must be **90+ days** (Strict).
2. **Price History:** Must have had at least **one price reduction** in the last 30 days.
3. **Price Cap:** Under **$450,000**.

**Required Data Columns (Excel Header)**
The client requires the following specific data points in the final CSV:

* **Full Address** (Street, City, State, Zip)
* **Current List Price**
* **Original List Price** (Must extract from listing history)
* **Total Discount %** (Calculated field: `(Original - Current) / Original * 100`)
* **Days on Market** (DOM)
* **Listing URL**

**Technical Constraints**

* **Output Format:** Clean Excel (`.xlsx`) or CSV.
* **Data Hygiene:** Zero duplicates.
* **Frequency:** Script must be reproducible (Client intends to run this weekly).