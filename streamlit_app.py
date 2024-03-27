import streamlit as st 
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


st.title("Delirium and Sepsis in Transgenic Mice Database")

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform queries.
#DataRepository = conn.query('SELECT * FROM DataRepository;', ttl=1)
#Intervention = conn.query('SELECT * FROM Intervention;', ttl=1)
#Mice = conn.query('SELECT * FROM Mice;', ttl=1)
Sequencing = conn.query('SELECT * FROM Sequencing;', ttl=1)
Study = conn.query('SELECT * FROM Study;', ttl=1)


# Print results.
#for row in Mice.itertuples():
#    st.write(row)



col1, col2 = st.columns([1,1])
with col1:
    disease_filter = st.multiselect("Disease Focus", options = conn.query("SELECT DISTINCT DiseaseFocus FROM Study;", ttl=1), 
                                    default=None)
with col2:
    name_filter = st.text_input("Sequencing Platform", placeholder="Enter Search")

select1 = ("SELECT Title,DiseaseFocus,Platform,DOI,URL,Journal,DatePub,ContactName,ContactEmail "
            "FROM Study AS st JOIN Sequencing AS seq ON seq.StudyID = st.StudyID WHERE ")

if disease_filter != []:
    for i in range(len(disease_filter)):
        if i == 0:
            select1 += f"(DiseaseFocus='{disease_filter[i]}'"
        else:
            select1 += f" OR DiseaseFocus='{disease_filter[i]}'"
    select1 += f") AND Platform LIKE '%{name_filter}%';"
else:
    select1 += f"Platform LIKE '%{name_filter}%';"


st.dataframe(conn.query(select1, ttl=1))

st.divider()


table_name = st.selectbox('Table', options=conn.query("""SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                                                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='MiceDB';"""))

select2 = select1.replace("SELECT ", "SELECT st.StudyID,")

df = conn.query(select2)

IDs = df[df.columns[0]]




filter = st.toggle("Use above filters")

if filter == False:
    st.dataframe(conn.query(f"Select * FROM {table_name};"))
else:
    select3 = "SELECT * FROM"
    
    for i in IDs:
        
        st.dataframe()



