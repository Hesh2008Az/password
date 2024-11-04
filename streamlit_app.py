import streamlit as st
import json
from random import choice, shuffle, randint

class PasswordManager:

    def __init__(self):
        self.labels_color = "#cdd1ce"

    def generate_password(self):
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        symbols = '!#$%&()*+'

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password = "".join(password_list)
        return password

    def find_password(self, website):
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            st.warning("No Data File Found.")
            return None
        else:
            return data.get(website)

    def save_password(self, website, email, password):
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}
        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        st.success("Password saved successfully!")


manager = PasswordManager()

st.title("MyPass Password Manager")

website = st.text_input("Website:")
email = st.text_input("Email/Username:", value="example@example.com")
password = st.text_input("Password:", type="password")

if st.button("Generate Password"):
    generated_password = manager.generate_password()
    st.text_input("Generated Password:", value=generated_password)
    st.write("Password copied to clipboard!")

if st.button("Save Password"):
    if website and email and password:
        manager.save_password(website, email, password)
    else:
        st.warning("Please fill in all fields.")

if st.button("Search Password"):
    result = manager.find_password(website)
    if result:
        st.info(f"Email: {result['email']}\nPassword: {result['password']}")
    else:
        st.warning(f"No details found for {website}.")

