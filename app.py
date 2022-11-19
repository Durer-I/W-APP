import streamlit as st
import pandas as pd
import sqlite3 
import numpy as np
from pathlib import Path
from datetime import datetime
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Workout",layout="wide")

current_path = Path.cwd()

class Workout():
    def __init__(self):
        self.connection = sqlite3.connect(current_path/'database.db')
        
        self.exercise_data = pd.read_sql(f"Select * FROM Exercises",self.connection)
        self.workout_data = pd.read_sql(f"Select * FROM Workouts",self.connection)

    def Get_Data(self,musclegroup):
        exercises = self.exercise_data.loc[self.exercise_data["Muscle_Group"].isin(musclegroup)]
        return exercises.Exercises.unique()

    def Add_Data(self,data=[]):
            buffer = pd.DataFrame()
            i = len(self.workout_data)
            buffer.loc[i,"Date"] = data[0]
            buffer.loc[i,"Muscle_Group"] = data[1]
            buffer.loc[i,"Exercise"] = data[2]
            buffer.loc[i,"Set_Type"] = data[3]
            buffer.loc[i,"Weight"] = data[4]
            buffer.loc[i,"Set_Number"] = data[5]
            buffer.loc[i,"Reps"] = data[6]
            buffer.to_sql("Workouts",self.connection,if_exists='append')

    def Visualization(self):
        pass

    def Add_Exercise(self,data):
        buffer=pd.DataFrame()
        i = len(self.exercise_data)
        buffer.loc[i,"Exercises"] = data[0]
        buffer.loc[i,"Muscle_group"] = data[1]
        buffer.to_sql("Exercises",self.connection,if_exists='append')

w=Workout()


decision = option_menu(menu_title=None, options=("Home","Log Workouts","Visualize Data","Add Exercises"),icons=['house',"box-arrow-in-right","graph-up-arrow","cloud-arrow-up-fill"],orientation='horizontal')

#start = st.date_input("Select the Start date for the backtest:",min_value=past,max_value=today,help="Please make sure the date is within 30 days if 1m is selected")
#end = st.date_input("Select the End date for the backtest:",min_value=past,max_value=today,help="Please make sure the date is within 30 days if 1m is selected")
#backtest = st.button("Start Backtesting",help="Click to start Backtesting")

muscle_groups = ['Chest','Back','Bicep','Triceps','Forearms','Neck','Quads','Hamstring','Calf','Abs','Shoulder']
muscle_groups.sort()
body_measuremnets = ['Weight','BMI','Fat%']

if decision == 'Home': pass

elif decision == 'Log Workouts': 
    with st.sidebar:
        
        workout = st.multiselect("Select Muscle Group",options = muscle_groups, help = "This allows you to add your workout")
        body = st.multiselect("Select Body Measurement:", options = body_measuremnets,help = "This allows you to add your body measurements")
        submit = st.button('Submit',help="Click to Submit")
    
    if 'display_flag' not in st.session_state: st.session_state.display_flag = True
    if submit: st.session_state.display_flag = False

        
    with st.form("Workout"):
        st.title("Select The exerceise to add data for:")

        exercise_data = w.Get_Data(musclegroup=workout)
        exercise = st.selectbox("Select Exercise to add Data", options = exercise_data,disabled=st.session_state.display_flag)
        
        st.header("Enter weight and set nukber and set type and rep number below")
        
        today = datetime. today()
        colb1,col_date,colb2=st.columns(3)
        with col_date : 
            workout_date = st.date_input("Workout Date:",max_value=today,help='Enter for which date the workout is for',disabled=st.session_state.display_flag)
            #sets = st.number_input("Enter number of sets:",min_value=1,step=1,disabled=st.session_state.display_flag)
        
        col1,col2,col3,col4 = st.columns(4)
        with col1: set_type = st.selectbox("Please select Set type:",options=("Warmup","Main"),disabled=st.session_state.display_flag)
        with col2: weight = st.number_input("Please add weight in lbs:",min_value=0,help='Weight here is in pounds',disabled=st.session_state.display_flag)
        with col3: set_number = st.number_input("Please enter set number",min_value=0,step=1,help='Enter which set data is this for',disabled=st.session_state.display_flag)
        with col4: rep_number = st.number_input("Please enter rep numbers",min_value=0,step=1,help='Enter which rep data is this for',disabled=st.session_state.display_flag)
        form_submit= st.form_submit_button("Submit",help='Enter data into database')
        
        if form_submit: 
            w.Add_Data(data=[workout_date,workout,exercise,set_type,weight,set_number,rep_number])
            st.success("Data Added to DataBase!!!")

elif decision == 'Visualize Data': 
    #w.workout_data
    
    st._legacy_dataframe(w.workout_data)

elif decision == 'Add Exercises':
    with st.form("Exercise",clear_on_submit=True):
        name = st.text_input("Please Enter Exercise Name")
        group = st.selectbox("Select Muscle Group",options = muscle_groups)

        exercise_submit = st.form_submit_button("Submit",help="Add exercise to the database")

    if exercise_submit: 
        w.Add_Exercise(data=[name,group])
        st.success("Data Added to DataBase!!!")
