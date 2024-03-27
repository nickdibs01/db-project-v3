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
#Sequencing = conn.query('SELECT * FROM Sequencing;', ttl=1)
#Study = conn.query('SELECT * FROM Study;', ttl=1)


# Print results.
#for row in Mice.itertuples():
#    st.write(row)



col1, col2 = st.columns([1,1])
with col1:
    disease_filter = st.multiselect("Disease Focus", 
                                    options = conn.query("SELECT DISTINCT DiseaseFocus FROM Study;", ttl=1), 
                                    default=None)
with col2:
    name_filter = st.text_input("Sequencing Platform", placeholder="Enter Search")

select1 = ("SELECT st.StudyID,Title,DiseaseFocus,Platform,DOI,URL,Journal,DatePub,ContactName,ContactEmail "
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

st.write("Studies that match your search:")
study_df = conn.query(select1, ttl=1)
st.dataframe(study_df, hide_index=True, 
             column_config={"URL": st.column_config.LinkColumn("URL")})

st.divider()


table_name = st.selectbox('Additional Study information', options=["Intervention", "Mice", "Sequencing"], index=2)

IDs = study_df[study_df.columns[0]]


filter = st.toggle("Use above filters")

pkeys = {"Intervention":"TreatmentID",
         "Mice":"MouseID"}

if filter == False:
    if table_name == "Sequencing":
        seq_df = conn.query("SELECT * FROM Sequencing;", ttl=1)
        seq_df["DataAvailable"] = seq_df["DataAvailable"].map({0: False, 1: True})
        st.dataframe(seq_df, hide_index=True)
    else:
        st.dataframe(conn.query(f"Select * FROM {table_name};", ttl=1).drop(pkeys[table_name], axis=1), 
                     hide_index=True)
elif len(IDs) == 0:
    st.write("Your search returned no results :slightly_frowning_face:")
else:
    select2 = f"SELECT * FROM {table_name} WHERE"
    first = True
    for i in IDs:
        if first == True:
            select2 += f" StudyID={i}"
            first = False
        else:
            select2 += f" OR StudyID={i}"
    select2 += ";"
    if table_name == "Sequencing":
        seq_df = conn.query(select2, ttl=1)
        seq_df["DataAvailable"] = seq_df["DataAvailable"].map({0: False, 1: True})
        st.dataframe(seq_df, hide_index=True)
    else:
        st.dataframe(conn.query(select2, ttl=1).drop(pkeys[table_name], axis=1), hide_index=True)


if table_name == "Sequencing" and len(IDs) != 0:
    st.write("Sequence Data")
    select3 = ("SELECT s.SequenceID,DataDescription,DatabaseName,AccessionNumber,URL FROM "
               "DataRepository AS dr JOIN Sequencing AS s ON dr.SequenceID=s.SequenceID WHERE ")
    first = True
    for i in IDs:
        if first == True:
            select3 += f" StudyID={i}"
            first = False
        else:
            select3 += f" OR StudyID={i}"
    select3 += ";"
    data_rep_df = conn.query(select3, ttl=1)
    if data_rep_df.empty:
        st.write("There are no available datasets for any of these sequences :slightly_frowning_face:")
    else:
        st.dataframe(data_rep_df, hide_index=True, column_config={"URL": st.column_config.LinkColumn("URL")})

