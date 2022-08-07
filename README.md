# Tracking the combat losses of Russia since the begiining of the inavsion with Ukraine
# VIDEO: 
#### Modules used:
- Streamlit
- Beautiful Soup
- Numpy
- Pandas
- Seaborn
- Matplotlib
#### Description:
This project uses the Streamlit. Streamlit is an open source app framework in Python language. 
It helps to create web apps for data science and machine learning in a short time.
The project scrapes the combat losses from the Minfin website (https://index.minfin.com.ua/en/russian-invading/casualties/).
The BeautifulSoup module is used for pulling data out of HTML files.
The extracted data is inserted into a Pandas dataframe, which is later saved in a local workspace.
This dataframe acts as an attribute of the ArmyLoss class.
The ArmyLoss class also has methods that are used to generated plots for the Streamlit app.
If the current day does not match the day of the last entry in the dataframe, the saved dataset is deleted, and an updated one is generated:
