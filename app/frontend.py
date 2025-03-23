import streamlit as st
import requests
from datetime import datetime
import uuid
import os
import json
import pandas as pd

# Set page title
st.set_page_config(page_title="Coffee Roasting & Cupping App", page_icon="☕")

# Update this at the top of your frontend.py
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8080')

# Add error handling for API calls
def api_call(endpoint, method='get', data=None):
    url = f"{BACKEND_URL}{endpoint}"
    try:
        if method == 'get':
            response = requests.get(url)
        elif method == 'post':
            response = requests.post(url, json=data)
        
        # Handle the response without debug messages
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                st.error(f"Error: Invalid response from server")
                return None
        else:
            st.error(f"Error: Server returned status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server")
        return None

# Title
st.title("☕ Coffee Roasting & Cupping App")

# Initialize session state if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Sidebar navigation
home_button = st.sidebar.button("🏠 Home")
roast_button = st.sidebar.button("🔥 Record Roast")
score_button = st.sidebar.button("📋 Score Coffee")
roast_history_button = st.sidebar.button("📚 Roast History")
cupping_history_button = st.sidebar.button("📊 Cupping History")

# Update current page based on button clicks
if home_button:
    st.session_state.current_page = "Home"
if roast_button:
    st.session_state.current_page = "Record Roast"
if score_button:
    st.session_state.current_page = "Score Coffee"
if roast_history_button:
    st.session_state.current_page = "Roast History"
if cupping_history_button:
    st.session_state.current_page = "Cupping History"

# Display content based on current page
if st.session_state.current_page == "Home":
    st.markdown("""
    ## 👋 Welcome to Your Coffee Journey!
    
    This app helps you track and evaluate your coffee roasts with professional precision.
    
    ### Features:
    - 🔥 **Record Roasts**: Track your roasting parameters including:
        - Agtron scores
        - Drop temperature
        - Development time
        - DTR ratio
    
    - 📋 **Score Coffee**: Evaluate your roasts using SCA standards:
        - Fragrance/Aroma
        - Flavor and Aftertaste
        - Acidity and Body
        - And more...
    
    ### Get Started
    Select an option from the sidebar to begin!
    """)

elif st.session_state.current_page == "Record Roast":
    st.header("🔥 Record Coffee Roast")
    
    with st.form("roast_form"):
        coffee_name = st.text_input("☕ Coffee Name")
        date = st.date_input("📅 Roast Date")
        
        col1, col2 = st.columns(2)
        with col1:
            agtron_whole = st.number_input("🌰 Agtron Whole Bean", 0, 100)
            agtron_ground = st.number_input("🏺 Agtron Ground", 0, 100)
            drop_temp = st.number_input("🌡️ Drop Temperature (°F)", 350.0, 450.0)
        
        with col2:
            development_time = st.number_input("⏱️ Development Time (minutes)", 0.0, 30.0)
            total_time = st.number_input("⏲️ Total Time (minutes)", 0.0, 30.0)
            dtr_ratio = st.number_input("📊 DTR Ratio", 0.0, 1.0)
        
        notes = st.text_area("📝 Roast Notes")
        
        if st.form_submit_button("💾 Save Roast"):
            data = {
                "roast_id": str(uuid.uuid4()),
                "date": str(date),
                "coffee_name": coffee_name,
                "agtron_whole": agtron_whole,
                "agtron_ground": agtron_ground,
                "drop_temp": drop_temp,
                "development_time": development_time,
                "total_time": total_time,
                "dtr_ratio": dtr_ratio,
                "notes": notes
            }
            
            result = api_call("/roasts/", method="post", data=data)
            if result:
                st.success("✅ Roast recorded successfully!")

elif st.session_state.current_page == "Score Coffee":
    st.header("📋 Coffee Cupping Score Sheet")
    
    # Get available roasts
    roasts = api_call('/roasts/')
    
    if roasts:
        # For databases/sqlalchemy response format (dictionary-like objects)
        # Create selection box for roasts
        roast_options = {f"{r['coffee_name']} - {r['date']}": r['roast_id'] for r in roasts}
        
        if roast_options:
            selected_roast = st.selectbox(
                "🔍 Select Coffee to Score",
                options=list(roast_options.keys())
            )
            
            if selected_roast:
                roast_id = roast_options[selected_roast]
                
                with st.form("scoring_form"):
                    date = st.date_input("📅 Cupping Date")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fragrance_aroma = st.slider("👃 Fragrance/Aroma", 0.0, 10.0, 6.0, 0.25)
                        flavor = st.slider("👅 Flavor", 0.0, 10.0, 6.0, 0.25)
                        aftertaste = st.slider("💭 Aftertaste", 0.0, 10.0, 6.0, 0.25)
                        acidity = st.slider("✨ Acidity", 0.0, 10.0, 6.0, 0.25)
                    
                    with col2:
                        body = st.slider("💪 Body", 0.0, 10.0, 6.0, 0.25)
                        uniformity = st.slider("🎯 Uniformity", 0.0, 10.0, 6.0, 0.25)
                        clean_cup = st.slider("✨ Clean Cup", 0.0, 10.0, 6.0, 0.25)
                        sweetness = st.slider("🍯 Sweetness", 0.0, 10.0, 6.0, 0.25)
                    
                    overall = st.slider("⭐ Overall", 0.0, 10.0, 6.0, 0.25)
                    defects = st.number_input("❌ Defects", 0, 100, 0)
                    notes = st.text_area("📝 Cupping Notes")

                    if st.form_submit_button("💾 Submit Score"):
                        total_score = (
                            fragrance_aroma + flavor + aftertaste + acidity + 
                            body + uniformity + clean_cup + sweetness + 
                            overall * 2 - defects
                        )
                        
                        data = {
                            "score_id": str(uuid.uuid4()),
                            "roast_id": roast_id,
                            "date": str(date),
                            "fragrance_aroma": fragrance_aroma,
                            "flavor": flavor,
                            "aftertaste": aftertaste,
                            "acidity": acidity,
                            "body": body,
                            "uniformity": uniformity,
                            "clean_cup": clean_cup,
                            "sweetness": sweetness,
                            "overall": overall,
                            "defects": defects,
                            "total_score": total_score,
                            "notes": notes
                        }
                        
                        result = api_call("/scores/", method="post", data=data)
                        if result:
                            st.success(f"✅ Score saved successfully! Total Score: {total_score:.2f}")
    else:
        st.warning("No roasts available to score. Please record a roast first.")

elif st.session_state.current_page == "Roast History":
    st.header("📚 Roast History")
    
    # Get roast data
    roasts = api_call('/roasts/')
    
    if roasts:
        # Create DataFrame
        df = pd.DataFrame(roasts)
        
        # Convert date strings to proper datetime format
        try:
            df['date'] = pd.to_datetime(df['date'])
        except:
            # Silently handle date conversion errors
            pass
        
        # Add filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            if 'coffee_name' in df.columns:
                coffee_options = sorted(df['coffee_name'].unique())
                coffee_filter = st.multiselect(
                    "Filter by Coffee Name",
                    options=coffee_options
                )
            else:
                coffee_filter = []
                
        with col2:
            if 'date' in df.columns:
                try:
                    min_date = df['date'].min().date() if not pd.isna(df['date'].min()) else datetime.now().date()
                    max_date = df['date'].max().date() if not pd.isna(df['date'].max()) else datetime.now().date()
                    date_range = st.date_input(
                        "Date Range",
                        value=(min_date, max_date)
                    )
                except:
                    date_range = None
            else:
                date_range = None
                
        # Apply filters
        if coffee_filter and 'coffee_name' in df.columns:
            df = df[df['coffee_name'].isin(coffee_filter)]
            
        if date_range and 'date' in df.columns and len(date_range) == 2:
            try:
                start_date = pd.Timestamp(date_range[0])
                end_date = pd.Timestamp(date_range[1])
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            except:
                # Silently handle date filtering errors
                pass
                
        # Display data
        st.subheader("Roast Records")
        if not df.empty:
            st.dataframe(
                df.sort_values('date', ascending=False) if 'date' in df.columns else df,
                hide_index=True
            )
            
            # Add download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Roast History",
                data=csv,
                file_name="coffee_roast_history.csv",
                mime="text/csv"
            )
        else:
            st.info("No records to display.")
    else:
        st.info("No roast records found.")

elif st.session_state.current_page == "Cupping History":
    st.header("📊 Cupping History")
    
    # Get cupping scores with detailed error handling
    scores = api_call('/scores/')
    
    if scores:
        # Create DataFrame with robust error handling
        try:
            df = pd.DataFrame(scores)
            
            # Convert date strings to proper datetime format
            if 'date' in df.columns:
                try:
                    df['date'] = pd.to_datetime(df['date'])
                except:
                    pass  # Silently handle the error
            
            # Get roast information to show coffee names
            roasts = api_call('/roasts/')
            if roasts:
                try:
                    roast_df = pd.DataFrame(roasts)
                    if 'roast_id' in roast_df.columns and 'coffee_name' in roast_df.columns:
                        roast_lookup = dict(zip(roast_df['roast_id'], roast_df['coffee_name']))
                        if 'roast_id' in df.columns:
                            df['coffee_name'] = df['roast_id'].map(roast_lookup)
                except Exception as e:
                    pass  # Skip the error message for non-critical issues
            
            # Add filters with robust error handling
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            with col1:
                if 'coffee_name' in df.columns:
                    coffee_options = sorted(df['coffee_name'].dropna().unique())
                    coffee_filter = st.multiselect(
                        "Filter by Coffee Name",
                        options=coffee_options
                    )
                else:
                    coffee_filter = []
                    
            with col2:
                if 'date' in df.columns:
                    try:
                        min_date = df['date'].min().date() if not pd.isna(df['date'].min()) else datetime.now().date()
                        max_date = df['date'].max().date() if not pd.isna(df['date'].max()) else datetime.now().date()
                        date_range = st.date_input(
                            "Date Range",
                            value=(min_date, max_date)
                        )
                    except:
                        date_range = None
                else:
                    date_range = None
            
            # Apply filters with error handling
            if coffee_filter and 'coffee_name' in df.columns:
                df = df[df['coffee_name'].isin(coffee_filter)]
                
            if date_range and 'date' in df.columns and len(date_range) == 2:
                try:
                    start_date = pd.Timestamp(date_range[0])
                    end_date = pd.Timestamp(date_range[1])
                    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                except:
                    pass  # Skip the error message for non-critical issues
            
            # Display data
            st.subheader("Cupping Scores")
            if not df.empty:
                st.dataframe(
                    df.sort_values('date', ascending=False) if 'date' in df.columns else df,
                    hide_index=True
                )
                
                # Add download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Cupping History",
                    data=csv,
                    file_name="coffee_cupping_history.csv",
                    mime="text/csv"
                )
            else:
                st.info("No records to display after filtering.")
        except Exception as e:
            pass  # Skip the error message for non-critical issues
    else:
        st.info("No cupping records found.") 