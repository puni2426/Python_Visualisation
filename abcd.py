# Selection box
import streamlit as st
st.title("Welcome, This is my first page")
st.header("form")
st.text_input("enter your name")
st.date_input("Enter your dOB")
radio_btn = st.radio("select your band:",('GT','E1','E2','E3'))
st.write("Your band is :",radio_btn)
select_btn = st.selectbox("Domain:",['Data Engineer','Linux','Kernel'])
st.write("Your domain is :", select_btn)
if st.button("Submit"):
	st.success("Submitted Successfully")


