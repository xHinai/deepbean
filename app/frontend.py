import streamlit as st
import requests
from datetime import datetime
import uuid
import pandas as pd
import time
import os

# Update this line at the top of your file
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

# Sidebar navigation
st.sidebar.title("☕ Navigation")
st.sidebar.markdown("---")

# Home button at the top of sidebar
home_button = st.sidebar.button("🏠 Home")
st.sidebar.markdown("---")
roast_button = st.sidebar.button("🔥 Record Roast")
score_button = st.sidebar.button("📋 Score Coffee")
roast_history_button = st.sidebar.button("📚 Roast History")
cupping_history_button = st.sidebar.button("📊 Cupping History")

# Initialize session state if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Update current page based on button clicks
if home_button:
    st.session_state.current_page = "Home"
    st.rerun()
if roast_button:
    st.session_state.current_page = "Record Roast"
    st.rerun()
if score_button:
    st.session_state.current_page = "Score Coffee"
    st.rerun()
if roast_history_button:
    st.session_state.current_page = "Roast History"
    st.rerun()
if cupping_history_button:
    st.session_state.current_page = "Cupping History"
    st.rerun()

# Main content area
st.title("☕ Blank Roasting & Cupping App")

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
            
            response = requests.post(f"{BACKEND_URL}/roasts/", json=data)
            if response.status_code == 200:
                st.success("✅ Roast recorded successfully!")

# Move the Return to Home button outside the form
if st.button("🏠 Return to Home"):
    st.session_state.current_page = "Home"
    st.rerun()

elif st.session_state.current_page == "Score Coffee":
    st.header("📋 Coffee Cupping Score Sheet")
    
    # Get available roasts
    response = requests.get(f"{BACKEND_URL}/roasts/")
    roasts = response.json()
    
    if roasts:
        # Create selection box for roasts
        roast_options = {f"{r[2]} - {r[1]}": r[0] for r in roasts}  # coffee_name - date: roast_id
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

                submit_button = st.form_submit_button("💾 Submit Score")
                if submit_button:
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
                    
                    response = requests.post(f"{BACKEND_URL}/scores/", json=data)
                    if response.status_code == 200:
                        st.success(f"✅ Score saved successfully! Total Score: {total_score:.2f}")
                    else:
                        st.error("Failed to save score. Please try again.")
    else:
        st.warning("No roasts available to score. Please record a roast first.")

elif st.session_state.current_page == "Roast History":
    st.header("📚 Roast History")
    
    # Get roast data
    response = requests.get(f"{BACKEND_URL}/roasts/")
    if response.status_code == 200:
        roasts = response.json()
        if roasts:
            # Convert to DataFrame for better display
            df = pd.DataFrame(roasts, columns=[
                'roast_id', 'date', 'coffee_name', 'agtron_whole', 
                'agtron_ground', 'drop_temp', 'development_time', 
                'total_time', 'dtr_ratio', 'notes'
            ])
            
            # Convert date strings to datetime
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # Add filters
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            with col1:
                coffee_filter = st.multiselect(
                    "Filter by Coffee Name",
                    options=sorted(df['coffee_name'].unique())
                )
            with col2:
                min_date = df['date'].min()
                max_date = df['date'].max()
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date) if min_date and max_date else None
                )
            
            # Apply filters
            if coffee_filter:
                df = df[df['coffee_name'].isin(coffee_filter)]
            if date_range:
                df = df[
                    (df['date'] >= date_range[0]) & 
                    (df['date'] <= date_range[1])
                ]
            
            # Display data
            st.subheader("Roast Records")
            st.dataframe(
                df.sort_values('date', ascending=False),
                hide_index=True,
                column_config={
                    'roast_id': None,  # Hide roast_id column
                    'date': st.column_config.DateColumn('Date'),
                    'coffee_name': 'Coffee Name',
                    'agtron_whole': 'Agtron (Whole)',
                    'agtron_ground': 'Agtron (Ground)',
                    'drop_temp': 'Drop Temp (°F)',
                    'development_time': 'Dev Time (min)',
                    'total_time': 'Total Time (min)',
                    'dtr_ratio': 'DTR Ratio',
                    'notes': 'Notes'
                }
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
            st.info("No roast records found.")
    else:
        st.error("Failed to fetch roast history.")

elif st.session_state.current_page == "Cupping History":
    st.header("📊 Cupping History")
    
    # Get cupping scores
    response = requests.get(f"{BACKEND_URL}/scores/")
    if response.status_code == 200:
        scores = response.json()
        if scores:
            # Convert to DataFrame
            df = pd.DataFrame(scores, columns=[
                'score_id', 'roast_id', 'date', 'fragrance_aroma',
                'flavor', 'aftertaste', 'acidity', 'body', 'uniformity',
                'clean_cup', 'sweetness', 'overall', 'defects',
                'total_score', 'notes'
            ])
            
            # Convert date strings to datetime
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # Get roast information to show coffee names
            roast_response = requests.get(f"{BACKEND_URL}/roasts/")
            if roast_response.status_code == 200:
                roasts = pd.DataFrame(roast_response.json(), columns=[
                    'roast_id', 'date', 'coffee_name', 'agtron_whole',
                    'agtron_ground', 'drop_temp', 'development_time',
                    'total_time', 'dtr_ratio', 'notes'
                ])
                roast_lookup = dict(zip(roasts['roast_id'], roasts['coffee_name']))
                df['coffee_name'] = df['roast_id'].map(roast_lookup)
            
            # Add filters
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            with col1:
                coffee_filter = st.multiselect(
                    "Filter by Coffee Name",
                    options=sorted(df['coffee_name'].unique())
                )
            with col2:
                min_date = df['date'].min()
                max_date = df['date'].max()
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date) if min_date and max_date else None
                )
            
            # Apply filters
            if coffee_filter:
                df = df[df['coffee_name'].isin(coffee_filter)]
            if date_range:
                df = df[
                    (df['date'] >= date_range[0]) & 
                    (df['date'] <= date_range[1])
                ]
            
            # Display data
            st.subheader("Cupping Scores")
            display_df = df.copy()
            st.dataframe(
                display_df.sort_values('date', ascending=False),
                hide_index=True,
                column_config={
                    'score_id': None,  # Hide score_id column
                    'roast_id': None,  # Hide roast_id column
                    'date': st.column_config.DateColumn('Date'),
                    'coffee_name': 'Coffee Name',
                    'fragrance_aroma': st.column_config.NumberColumn('Fragrance/Aroma', format="%.2f"),
                    'flavor': st.column_config.NumberColumn('Flavor', format="%.2f"),
                    'aftertaste': st.column_config.NumberColumn('Aftertaste', format="%.2f"),
                    'acidity': st.column_config.NumberColumn('Acidity', format="%.2f"),
                    'body': st.column_config.NumberColumn('Body', format="%.2f"),
                    'uniformity': st.column_config.NumberColumn('Uniformity', format="%.2f"),
                    'clean_cup': st.column_config.NumberColumn('Clean Cup', format="%.2f"),
                    'sweetness': st.column_config.NumberColumn('Sweetness', format="%.2f"),
                    'overall': st.column_config.NumberColumn('Overall', format="%.2f"),
                    'defects': 'Defects',
                    'total_score': st.column_config.NumberColumn('Total Score', format="%.2f"),
                    'notes': 'Notes'
                }
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
            st.info("No cupping records found.")
    else:
        st.error("Failed to fetch cupping history.") 