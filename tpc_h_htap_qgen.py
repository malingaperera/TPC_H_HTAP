import os

# Set the query folder and output folder. Copy the created files from TPC-H data generator into query folder.
# Note: deletes.0 file generated from TPC-H Skew generator was different to other delete files and therefor that file
# was not copied.
output_folder = "output\\"
query_folder = "tpc_h_data\\"

# write 'w', append 'a+'
file_open_mood = 'w+'

# Every query type will cover both lineitem and order tables. So the total number of each query will be twice the size
# defined here.
inserts_per_table = 50
deletes_per_table = 50
updates_per_table = 50

# first we will read in the data that need to populate the queries (make sure you have generated enough files/data rows)
deletes_raw = []
inserts_raw = {"order": [], "lineitem": []}


delete_files = os.listdir(query_folder + 'deletes\\')
li_insert_files = [f for f in os.listdir(query_folder + 'inserts\\') if f.startswith('lineitem')]
o_insert_files = [f for f in os.listdir(query_folder + 'inserts\\') if f.startswith('order')]

# We won't read all the files, but only enough data points to generate the defined number of queries
current_file = 0
while len(deletes_raw) < deletes_per_table:
    with open( query_folder + 'deletes\\' + delete_files[current_file]) as f:
        deletes_raw.extend(f.readlines())
    current_file += 1

current_file = 0
while len(inserts_raw["order"]) < (inserts_per_table + updates_per_table):
    with open(query_folder + 'inserts\\' + li_insert_files[current_file]) as f_lineitem, \
            open(query_folder + 'inserts\\' + o_insert_files[current_file]) as f_order:
        inserts_raw["lineitem"].extend(f_lineitem.readlines())
        inserts_raw["order"].extend(f_order.readlines())
    current_file += 1


def get_deletes():
    """
    Write the deletes.sql

    We have used SQL server syntax, make sure you change based on your database type.
    """

    deletes = [
        "delete from lineitem where l_orderkey = {};",
        "delete from orders where o_orderkey = {};"
    ]
    with open(output_folder + "deletes.sql", file_open_mood) as o_file:
        for d_id in range(deletes_per_table):
            for q_string in deletes:
                o_file.write(q_string.format(deletes_raw[d_id].split('\n')[0]))
                o_file.write('\n')


def get_inserts():
    """
    Write the inserts.sql

    We have used SQL server syntax, make sure you change based on your database type.
    """
    inserts = {
        "i_1": "insert into orders values ({}, {}, '{}', {}, '{}', '{}', '{}', {}, '{}');",
        "i_2": "insert into lineitem values ({}, {}, {}, {}, {}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' );"
    }

    with open(output_folder + "inserts.sql", file_open_mood) as o_file:
        for i_id in range(inserts_per_table):
            o_file.write(
                inserts["i_1"].format(*inserts_raw["order"][i_id].split('|')))
            o_file.write('\n')
            o_file.write(
                inserts["i_2"].format(*inserts_raw["lineitem"][i_id].split('|')))
            o_file.write('\n')


def get_updates():
    """
    Write the updates.sql

    We have used SQL server syntax, make sure you change based on your database type.
    """
    updates = {
        "u_1":
"""UPDATE [dbo].[ORDERS]
    SET [O_CUSTKEY] = {1}
      ,[O_ORDERSTATUS] = '{2}'
      ,[O_TOTALPRICE] = {3}
      ,[O_ORDERDATE] = '{4}'
      ,[O_ORDERPRIORITY] = '{5}'
      ,[O_CLERK] = '{6}'
      ,[O_SHIPPRIORITY] = {7}
      ,[O_COMMENT] = '{8}'
    WHERE [O_ORDERKEY] = {0};
""",
        "u_2":
"""UPDATE [dbo].[LINEITEM]
   SET [L_QUANTITY] = {4}
      ,[L_EXTENDEDPRICE] = {5}
      ,[L_DISCOUNT] = {6}
      ,[L_TAX] = {7}
      ,[L_RETURNFLAG] = '{8}'
      ,[L_LINESTATUS] = '{9}'
      ,[L_SHIPDATE] = '{10}'
      ,[L_COMMITDATE] = '{11}'
      ,[L_RECEIPTDATE] = '{12}'
      ,[L_SHIPINSTRUCT] = '{13}'
      ,[L_SHIPMODE] = '{14}'
      ,[L_COMMENT] = '{15}'
    WHERE [L_ORDERKEY] = {0} and [L_LINENUMBER] = 1;
"""
    }
    with open(output_folder + "updates.sql", file_open_mood) as o_file:
        for u_id in range(updates_per_table):
            delete_id = deletes_raw[inserts_per_table + u_id].split('\n')[0]

            params = inserts_raw["order"][inserts_per_table + u_id].split('|')
            params[0] = delete_id
            o_file.write(updates["u_1"].format(*params))
            o_file.write('\n')

            params = inserts_raw["lineitem"][inserts_per_table + u_id].split('|')
            params[0] = delete_id
            o_file.write(updates["u_2"].format(*params))
            o_file.write('\n')


# generate the files
get_inserts()
get_deletes()
get_updates()
