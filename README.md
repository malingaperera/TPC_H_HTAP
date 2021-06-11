# TPC-H and TPC-H Skew HTAP Workload
This project helps you to create INSERT, DELETE and UPDATE queries for TPC-H and TPC-H Skew.

There isn't any proper HTAP workload with skewed datasets. There for I have generated INSERT, DELETE and UPDATE queries for TPC-H Skew. This can be used with TPC-H as well.

## How to setup TPC-H Skew (TPC-H setup is similar)

Initially you need to have the TPCH-Skew setup 

Download and Build the project.: https://www.microsoft.com/en-us/download/details.aspx?id=52430

I assume you already have a working project and have already generated data for your database.

Here we will discuss how you can generate INSERT, DELETE and UPDATE queries for TPC-H Skew.

datagen.exe can be used to generate data required for the queries

1. Generating seeds (remember to use same scale factor as your database -s)
`./Debug/dbgen -v -O s -s 10`
2. Data generation
`./Debug/dbgen -v -U 2 -s 10`
3. Copy the generated files into `tpc_h_data` folder
4. Edit the SQL syntax in the `tpc_h_htap_qgen.py` based on your database type (SQL Server is already provided)
5. Edit the input and output folder paths if needed.
6. Run `tpc_h_htap_qgen.py` 

