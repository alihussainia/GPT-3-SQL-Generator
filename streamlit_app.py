# -*- coding: utf-8 -*-
"""
Created on Sunday June 26 2022
@author: Muhammad Ali
@github: @alihussainia
"""

import streamlit as st
from api import GPT, Example, set_openai_key
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

st.set_page_config(page_title="SQL Generator", layout='centered', initial_sidebar_state='auto', menu_items=None)

st.title("SQL Generator Application")
st.write("A web app that generates SQL queries using plain English")

inp = st.text_area("Please enter your query here", max_chars=2000, height=150)

# Get environment variables
key = os.getenv('key')
set_openai_key(key)

#Construct GPT-3-instruct instance, add instruction and examples
gpt = GPT(engine="davinci-instruct-beta",
          temperature=0.3,
          max_tokens=200)
gpt.add_instruction('Given an input question, respond with syntactically correct PostgreSQL.')

gpt.add_example(Example('select columns from users table', 
                        'select id, email, dt, plan_type, created_on, updated_on from users'))
gpt.add_example(Example('select columns from the charges table', 
                        'select amount, amount_refunded, created, customer_id, status from charges'))
gpt.add_example(Example('select columns from the customers table', 
                        'select created, email, id from customers'))
gpt.add_example(Example('how many users signed up in the past 30 days?', 
                        "SELECT COUNT(*) FROM users WHERE signup_dt >= now() - interval '30 days'"))
gpt.add_example(Example('when did user with email brian@seekwell.io sign up?', 
                        "SELECT signup_dt FROM users WHERE email = 'brian@seekwell.io'"))
gpt.add_example(Example('how much revenue did we have in the past 7 days?', 
                        "SELECT SUM(amount) from charges WHERE charge_dt >= now() - interval '7 days'"))
gpt.add_example(Example('how many users signed up in the past 30 days?', 
                        "SELECT COUNT(*) FROM users WHERE signup_dt >= now() - interval '30 days'"))
gpt.add_example(Example('how much revenue did we have from 10-01-20 through 11-15-20?', 
                        "SELECT SUM(case when charge_dt>= '10-01-20'::date and charge_dt < '11-15-20'::date then amount else 0 end) as revenue FROM charges"))
gpt.add_example(Example('how much revenue have we had from users that signed up in the last 6 months?', 
                        "SELECT SUM(charges.amount) FROM users INNER JOIN charges ON users.id = charges.user_id WHERE users.signup_dt>= now() - interval '6 months'"))
gpt.add_example(Example('when did user with email brian@seekwell.io make his first payment?', 
                        "SELECT MIN(charge_dt) as last_payment_dt from users INNER JOIN charges ON users.id = charges.user_id WHERE users.email = 'brian@seekwell.io'"))
gpt.add_example(Example('how many new users signed up in each of the last 2 months?', 
                        "SELECT sum(case when signup_dt>= now() - interval '1 month' then 1 else 0 end) as signups_this_month, sum(case when signup_dt>= now() - interval '2 months' and signup_dt < now() - interval '1 month'  then 1 else 0 end) as signups_last_month FROM users"))

submit_button = st.button('Generate')

if submit_button and inp=="":
  st.write("Please enter your problem above")

elif submit_button and inp!="":
  output = gpt.submit_request(inp.value)
  result = output['choices'][0].text
  query = result.split('output:')[1]
  st.markdown(query) 


st.text("App developed with ❤️ by @alihussainia")

st.text(f"Connect with me via Email at malirashid1994@gmail.com")