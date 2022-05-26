import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as py
import streamlit as st
import seaborn as sns
import os
#from PIL import image
st.set_option('deprecation.showPyplotGlobalUse', False)

# Title
st.title("Cellulant Remittance EDA App")
st.header("Built with streamlit")

# Connecting to the database
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", database="remittance_db")

mycursor = mydb.cursor(dictionary = True)
#mycursor.execute("select * from hub_tz")
#counter = 0 
#limit = 6 
#for i in mycursor:
#    counter = counter + 1
#    if counter == limit :
#        break 
#    print(i)

 # DataFrame
 
#data = pd.DataFrame(mycursor)
#data.to_csv (r'C:\Users\User\Documents\streamlit', index = False)

# Dataframe
#my_dataset = 'hub_tz.csv'


# Function to load dataset
#@st.cache(persist = True)
#def explore_data(dataset):
#    df = pd.read_csv(os.path.join(dataset))
#    return df

#data = explore_data(my_dataset)
#data = data_df.drop(columns = ["Beep Transaction ID","Customer Mobile Number"])    

#numerical_variables_df = data.select_dtypes(exclude=['object'])
#numerical_variables_df = numerical_variables_df.drop(columns = ['Beep Transaction ID','Customer Mobile Number'])

#categorical_variables_df = data.select_dtypes(include = ['object'])

def main():

# Sidebar

	st.sidebar.subheader("Visualization Settings")
	
	menu = ["Tanzania", "Malawi"]
	choice = st.sidebar.selectbox("Countries", menu)

	if choice == "Tanzania":
		#data = pd.read_csv("hub_tz.csv")
		mycursor.execute("select * from hub_tz")
		data = pd.DataFrame(mycursor)
		st.subheader("Tanzania Data")
		#st.write(data.head(2))

	elif choice == "Malawi":
		#data = pd.read_csv("hub_mw.csv")
		mycursor.execute("select * from hub_mw")
		data = pd.DataFrame(mycursor)
		st.subheader("Malawi Data")
		#st.write(data.head(2))


	numerical_variables_df = data.select_dtypes(exclude=['object'])
	numerical_variables_df = numerical_variables_df.drop(columns = ['BeepTransactionID','CustomerMobileNumber'])

	categorical_variables_df = data.select_dtypes(include = ['object'])



# Sidebar

	menu = ["Overview", "Main_Dataset", "Services", "Clients"]
	choice = st.sidebar.selectbox("Analysis", menu)

	# Overview of the dataset

	if choice == "Overview":
		st.subheader("Overview of the Dataset")
		if st.checkbox("Preview Dataset"):
			#data = explore_data(my_datase
			if st.button("Head"):
				st.write(data.head())
			if st.button("Tail"):
				st.write(data.tail())
			else:
				st.write(data.head(2))

		# show entire dataset
		if st.checkbox("Show Entire Dataset"):
			#st.write(data)
			st.dataframe(data)

		# Show column names
		if st.checkbox("Show Column Names"): 
			st.write(data.columns)

		# Show dimensions
		data_dim = st.radio("What Dimensions Do You Want to See?", ("Rows", "Columns", "All"))
		if data_dim == 'Rows':
			st.text('Showing Rows')
			st.write(data.shape[0])

		elif data_dim == 'Columns':
			st.text('Showing Columns')
			st.write(data.shape[1])

		else:
			st.text("Shape of the Dataset")
			st.write(data.shape)

# EDA of whole dataset

	elif choice == "Main_Dataset":
		st.subheader("Analysis of the whole dataset")

		# Show decriptive statistics
		if st.checkbox("Show Descriptive Statistics of the Dataset"):
			st.write(numerical_variables_df.describe())

		# The row and columns with high TAT
		if st.checkbox("Row with Highest Total TAT"):
			#st.write(data[data['Total TAT'] == 3595])
			TAT = data.sort_values(by=['TotalTAT'],ascending=[ False])
			st.write(TAT.head(10))

		# Rows with TAT of above 100
		#if st.checkbox("Rows with Total TAT of Above 100"):
		#	st.write(data[data['Total TAT'] > 100].sort_values(by=['Total TAT'],ascending=[ False]))
		

		# Univariate Analysis

		st.subheader("Univariate Analysis")

		#plt.figure(figsize = (2,2))


		# Traffic Analysis
		st.subheader("Traffic Analysis")

		if st.checkbox("Number of Request By Time of Day"):
			df_date = data.filter(['DateCreated'])
			df_date["DateCreated"] = pd.to_datetime(df_date["DateCreated"])
			hr = df_date["DateCreated"].dt.hour
			minute = df_date["DateCreated"].dt.minute
			sec = df_date["DateCreated"].dt.second

			df_date['hour'] = hr
			df_date['minute'] = minute
			df_date['second'] = sec

			group = df_date.groupby('hour')
			req = group['hour'].agg('count')
			req_df=pd.DataFrame(req)

			req_df.rename(
				columns={
				    'hour':'#_requests',
				},
				inplace = True
				)
			req_df.reset_index(inplace=True)

			st.write(py.bar(req_df, x = 'hour', y = '#_requests'))
			if st.checkbox("Traffic Analysis Line graph"):
				st.write(py.line(req_df, x = 'hour', y = '#_requests'))



		# Status Analysis
		st.subheader("Status Analysis")

		if st.checkbox("Status Synched"):
			status_synched = data['StatusSynced'].value_counts(normalize = False)
			st.write(status_synched)
			if st.checkbox('Graph of Synced Status '):
				st.write(py.bar(status_synched))
				#st.pyplot()

		if st.checkbox("Final Status"):
			final_status = data['FinalStatus'].value_counts(normalize = False)
			st.write(final_status)
			if st.checkbox("Graph of Final Status"):
				st.write(py.bar(final_status))
				#st.pyplot()
		

		if st.checkbox("Manually Reconciled"):
			m_recon = data['ManuallyReconciled'].value_counts(normalize = False)
			st.write(m_recon)
			if st.checkbox("Graph of Manually Reconciled "):
				st.write(py.bar(['m_recon']))
				#st.pyplot()


		# Bivariate Analysis

		# Service Name column
		st.subheader("Bivariate Analysis")
		col_option = st.selectbox('Select Column',("Service Name", "Client Name"))

		if col_option == 'Service Name':
			services_num = data['ServiceName'].value_counts()
			st.write(services_num)
			if st.checkbox('Graph of Service Names '):
				st.write(py.bar(services_num))
				#st.pyplot()	

		# Client Name Column	
		elif col_option == 'Client Name':
			clients_num = data['ClientName'].value_counts()
			st.write(clients_num)
			if st.checkbox('Graph of Client Names '):
				st.write(py.bar(clients_num))
				#st.pyplot()

		else:
			st.write("Select Column")



		# Rows with failed and pending status
		st.subheader(" Rows with Failed and Pending Status")

		# Check the failed status
		if st.checkbox("Rows with Failed Status"):
			data[data['FinalStatus'] == 'FAILED']

		# Check for pending status
		if st.checkbox("Rows with Pending Status"):
			data[data['FinalStatus'] == 'PENDING']




		# Average Amount paid and total TAT

		st.subheader("Average Amount paid and total TAT")

		if st.checkbox("Average Amount Paid per Service"):
			ServiceAvgAmount = data.groupby(["ServiceName"], as_index = False)['AmountPaid'].mean().sort_values(by = "AmountPaid", ascending = False)
			st.write(ServiceAvgAmount)
			if st.checkbox("Graph of Avg Amount Paid per Service"):
				st.write(py.bar(ServiceAvgAmount, x = "ServiceName", y = "AmountPaid"))
				#ServiceAvgAmount.sort_values(ascending=False).plot.bar(figsize=(10, 5), grid = True)
				#st.pyplot()

		if st.checkbox("Average Amount Paid per Client"):
			ClientAvgAmount = data.groupby(["ClientName"], as_index = False)['AmountPaid'].mean().sort_values(by = "AmountPaid", ascending = False)
			st.write(ClientAvgAmount)
			if st.checkbox("Graph of Avg Amount Paid per Client"):
				st.write(py.bar(ClientAvgAmount, x = "ClientName", y = "AmountPaid"))				
				#ClientAvgAmount.sort_values(ascending=False).plot.bar(figsize=(10, 5), grid = True)
				#st.pyplot()

		# Average Total TAT

		if st.checkbox("Average Total TAT per Service"):
			serviceAvgTAT = data.groupby(["ServiceName"], as_index = False)['TotalTAT'].mean().sort_values(by = "TotalTAT", ascending = False)
			st.write(serviceAvgTAT)
			if st.checkbox("Graph Average Total TAT per Service"):
				st.write(py.bar(serviceAvgTAT, x = "ServiceName", y = "TotalTAT"))
				#serviceAvgTAT.sort_values(ascending=False).plot.bar(figsize=(10, 5), grid = True)
				#st.pyplot()

		if st.checkbox("Average Total TAT per Client"):
			clientAvgTAT = data.groupby(["ClientName"], as_index = False)['TotalTAT'].mean().sort_values(by = "TotalTAT", ascending = False)
			st.write(clientAvgTAT)
			if st.checkbox("Graph Average Total TAT per Client"):
				st.write(py.bar(clientAvgTAT, x = "ClientName", y = "TotalTAT"))
				#clientAvgTAT.sort_values(ascending=False).plot.bar(figsize=(10, 5), grid = True)
				#st.pyplot()

		# Correlation
		st.subheader("Correlation")
		
		if st.checkbox("Show Correlation"):
			st.write(numerical_variables_df.corr())
			matrix = numerical_variables_df.corr()
			if st.checkbox("Correlation Heatmap"):
				st.write(py.imshow(matrix))
				#st.pyplot()		




# Analysis by Service Name

	elif choice == "Services":
		st.subheader("EDA by Service Name")
		
		services = data['ServiceName'].unique().tolist()
		#if type(services) == list:
		#    print("Hello

		def perfom_service_analysis(services_list):
			for service in services:
				if st.checkbox(service):
					df_service = data.loc[data['ServiceName']== service]
					df_service = df_service.drop(columns = ['BeepTransactionID','CustomerMobileNumber'])
					st.write(df_service.describe())
					st.write(df_service['StatusSynced'].value_counts(normalize = False))
					st.write(df_service['FinalStatus'].value_counts(normalize = False))
					st.write(df_service['ManuallyReconciled'].value_counts(normalize = False))
					st.write(df_service['ClientName'].value_counts())

		perfom_service_analysis(services)


 # Analysis by Client Name           

	elif choice == "Clients":
		st.subheader("EDA by Client Name")
		clients = data['ClientName'].unique().tolist()
		#if type(clients) == list:
		#    print("Hello")

		def perfom_service_analysis(clients_list):
			for client in clients:
				if st.checkbox(client):
					df_client = data.loc[data['ClientName']== client]
					df_client = df_client.drop(columns = ['BeepTransactionID','CustomerMobileNumber'])					
					st.write(df_client.describe())
					st.write(df_client['StatusSynced'].value_counts(normalize = False))
					st.write(df_client['FinalStatus'].value_counts(normalize = False))
					st.write(df_client['ManuallyReconciled'].value_counts(normalize = False))
					st.write(df_client['ServiceName'].value_counts())

		perfom_service_analysis(clients)
				

	else:
		st.subheader("About")
		

if __name__ == '__main__':
	main()

