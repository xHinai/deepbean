import streamlit as st
import requests
from datetime import datetime
import uuid
import os
import json
import pandas as pd
import altair as alt

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
            drop_temp = st.number_input(
                "🌡️ Drop Temperature (°C)",
                min_value=180.0,
                max_value=240.0,
                value=210.0,
                step=0.5
            )
        
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
        
        # Reorder columns to put coffee_name first and drop the roast_id
        if 'coffee_name' in df.columns:
            # Define column order with coffee_name first
            cols = ['coffee_name', 'date', 'agtron_whole', 'agtron_ground', 'drop_temp',
                   'development_time', 'total_time', 'dtr_ratio', 'notes']
            
            # Keep only columns that exist in the dataframe
            available_cols = [col for col in cols if col in df.columns]
            
            # Reorder dataframe
            df = df[available_cols]
        
        # Add filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'coffee_name' in df.columns:
                coffee_options = sorted(df['coffee_name'].unique())
                selected_coffees = st.multiselect(
                    "Filter by Coffee Name",
                    options=coffee_options
                )
                
                if selected_coffees:
                    df = df[df['coffee_name'].isin(selected_coffees)]
        
        with col2:
            if 'date' in df.columns:
                try:
                    # Convert to datetime first
                    df['date'] = pd.to_datetime(df['date'])
                    min_date = df['date'].min().date()
                    max_date = df['date'].max().date()
                    
                    date_range = st.date_input(
                        "Date Range",
                        value=(min_date, max_date),
                        key="roast_date_range"
                    )
                    
                    if len(date_range) == 2:
                        start_date = pd.Timestamp(date_range[0])
                        end_date = pd.Timestamp(date_range[1])
                        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                except Exception as e:
                    pass
        
        # Display data
        st.subheader("Roast Records")
        if not df.empty:
            # Use a wider layout for the table
            st.dataframe(
                df.sort_values('date', ascending=False) if 'date' in df.columns else df,
                hide_index=True,
                use_container_width=True  # Make the table use the full width
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
            st.info("No records to display after filtering.")
    else:
        st.info("No roast records found.")

elif st.session_state.current_page == "Cupping History":
    st.header("📊 Cupping History")
    
    # Get cupping scores
    scores = api_call('/scores/')
    
    if scores:
        # Create DataFrame
        df = pd.DataFrame(scores)
        
        # Get roast information to show coffee names
        roasts = api_call('/roasts/')
        if roasts:
            roast_df = pd.DataFrame(roasts)
            roast_lookup = dict(zip(roast_df['roast_id'], roast_df['coffee_name']))
            df['coffee_name'] = df['roast_id'].map(roast_lookup)
        
        # Reorder columns to put coffee_name first and drop the IDs
        if 'coffee_name' in df.columns:
            # Define the desired column order with coffee_name first
            cols = ['coffee_name', 'date', 'fragrance_aroma', 'flavor', 'aftertaste', 'acidity', 
                   'body', 'uniformity', 'clean_cup', 'sweetness', 'overall', 'defects', 
                   'total_score', 'notes']
            
            # Keep only columns that exist in the dataframe
            available_cols = [col for col in cols if col in df.columns]
            
            # Reorder dataframe
            df = df[available_cols]
        
        # Add filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'coffee_name' in df.columns:
                coffee_options = sorted(df['coffee_name'].unique())
                selected_coffees = st.multiselect(
                    "Filter by Coffee Name",
                    options=coffee_options
                )
                
                if selected_coffees:
                    df = df[df['coffee_name'].isin(selected_coffees)]
        
        with col2:
            if 'date' in df.columns:
                try:
                    # Convert to datetime first
                    df['date'] = pd.to_datetime(df['date'])
                    min_date = df['date'].min().date()
                    max_date = df['date'].max().date()
                    
                    date_range = st.date_input(
                        "Date Range",
                        value=(min_date, max_date),
                        key="cupping_date_range"
                    )
                    
                    if len(date_range) == 2:
                        start_date = pd.Timestamp(date_range[0])
                        end_date = pd.Timestamp(date_range[1])
                        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                except Exception as e:
                    pass
        
        # Display data
        st.subheader("Cupping Scores")
        if not df.empty:
            # Use a wider layout for the table
            st.dataframe(
                df.sort_values('date', ascending=False) if 'date' in df.columns else df,
                hide_index=True,
                use_container_width=True  # Make the table use the full width
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
    else:
        st.info("No cupping records found.")

# If the check is in a section where drop_temp might not be defined
if 'drop_temp' in locals() or 'drop_temp' in globals():  # Check if the variable exists
    if drop_temp < 180 or drop_temp > 240:
        st.warning("Drop temperature outside normal range for Celsius (180°C - 240°C)")

# Add the Green Beans page content
elif st.session_state.current_page == "Green Beans":
    st.header("🌱 Green Bean Inventory")
    
    # Create tabs for adding new beans and viewing inventory
    tab1, tab2 = st.tabs(["Add New Beans", "View Inventory"])
    
    with tab1:
        st.subheader("Record New Green Beans")
        
        with st.form("new_green_bean_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Coffee Name")
                origin = st.text_input("Origin")
                processing = st.selectbox(
                    "Processing Method",
                    options=["Washed", "Natural", "Honey", "Anaerobic", "Other"]
                )
                variety = st.text_input("Variety")
                altitude = st.text_input("Altitude")
            
            with col2:
                purchase_date = st.date_input("Purchase Date")
                initial_stock_kg = st.number_input("Initial Stock (kg)", min_value=0.1, value=60.0)
                price_per_kg = st.number_input("Price per kg", min_value=0.0, value=10.0)
                supplier = st.text_input("Supplier")
                
            notes = st.text_area("Notes")
            
            if st.form_submit_button("📝 Save Green Bean"):
                if not name:
                    st.error("Coffee name is required!")
                else:
                    # Create green bean record
                    green_bean_data = {
                        "name": name,
                        "origin": origin,
                        "processing": processing,
                        "variety": variety,
                        "altitude": altitude,
                        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                        "initial_stock_kg": initial_stock_kg,
                        "current_stock_kg": initial_stock_kg,  # Initialize current stock equal to initial
                        "price_per_kg": price_per_kg,
                        "supplier": supplier,
                        "notes": notes
                    }
                    
                    # Send to API
                    result = api_call("/green-beans/", method="post", data=green_bean_data)
                    
                    if result and "bean_id" in result:
                        st.success("Green beans added successfully!")
                    else:
                        st.error("Error adding green beans!")
    
    with tab2:
        st.subheader("Green Bean Inventory")
        
        # Get green bean data
        green_beans = api_call('/green-beans/')
        
        if green_beans:
            # Create DataFrame
            df = pd.DataFrame(green_beans)
            
            # Add filters
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            
            with col1:
                if 'name' in df.columns:
                    coffee_options = sorted(df['name'].unique())
                    selected_coffees = st.multiselect(
                        "Filter by Coffee Name",
                        options=coffee_options
                    )
                    
                    if selected_coffees:
                        df = df[df['name'].isin(selected_coffees)]
            
            with col2:
                if 'origin' in df.columns:
                    origin_options = sorted(df['origin'].unique())
                    selected_origins = st.multiselect(
                        "Filter by Origin",
                        options=origin_options
                    )
                    
                    if selected_origins:
                        df = df[df['origin'].isin(selected_origins)]
            
            # Show stock status with color coding
            if 'current_stock_kg' in df.columns and 'initial_stock_kg' in df.columns:
                # Calculate percentage of stock remaining
                df['stock_percent'] = (df['current_stock_kg'] / df['initial_stock_kg'] * 100).round(1)
                
                # Add status column
                def get_status(percent):
                    if percent <= 10:
                        return "Critical"
                    elif percent <= 25:
                        return "Low"
                    elif percent <= 50:
                        return "Medium"
                    else:
                        return "Good"
                
                df['status'] = df['stock_percent'].apply(get_status)
                
                # Display stock overview
                st.subheader("Stock Overview")
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                # Set up colors for the statuses
                colors = {
                    'Critical': '#FF5252',
                    'Low': '#FFC107',
                    'Medium': '#2196F3',
                    'Good': '#4CAF50'
                }
                
                # Display as a bar chart
                status_chart = alt.Chart(status_counts).mark_bar().encode(
                    x=alt.X('Status:N', sort=['Critical', 'Low', 'Medium', 'Good']),
                    y='Count:Q',
                    color=alt.Color('Status:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values())))
                ).properties(width=600)
                
                st.altair_chart(status_chart, use_container_width=True)
            
            # Show only relevant columns and hide bean_id
            display_cols = ['name', 'origin', 'processing', 'variety', 'purchase_date', 
                           'initial_stock_kg', 'current_stock_kg', 'stock_percent', 'status',
                           'price_per_kg', 'supplier', 'notes']
            
            # Keep only columns that exist in the dataframe
            display_cols = [col for col in display_cols if col in df.columns]
            
            # Display the inventory
            if not df.empty:
                # Style the dataframe
                def highlight_status(val):
                    if val == 'Critical':
                        return 'background-color: #FFEBEE'
                    elif val == 'Low':
                        return 'background-color: #FFF8E1'
                    elif val == 'Medium':
                        return 'background-color: #E3F2FD'
                    elif val == 'Good':
                        return 'background-color: #E8F5E9'
                    return ''
                
                if 'status' in display_cols:
                    styled_df = df[display_cols].style.apply(
                        lambda x: x.map(highlight_status) if x.name == 'status' else [''] * len(x),
                        axis=0
                    )
                    st.dataframe(styled_df, hide_index=True, use_container_width=True)
                else:
                    st.dataframe(df[display_cols], hide_index=True, use_container_width=True)
                
                # Add download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Inventory",
                    data=csv,
                    file_name="green_bean_inventory.csv",
                    mime="text/csv"
                )
            else:
                st.info("No inventory records to display after filtering.")
        else:
            st.info("No green beans found in inventory.")

# Update the New Roast section to use green bean inventory
elif st.session_state.current_page == "New Roast":
    st.header("☕ Log New Coffee Roast")
    
    # Get green bean inventory for selection
    green_beans = api_call('/green-beans/')
    
    # Form for new roast
    with st.form("new_roast_form"):
        # If we have green beans in inventory
        if green_beans:
            # Create a dictionary for selection: display name -> bean_id
            bean_options = {f"{bean['name']} ({bean['origin']}) - {bean['current_stock_kg']}kg available": 
                            bean['bean_id'] for bean in green_beans}
            
            # Default to the first bean if available
            default_bean = list(bean_options.keys())[0] if bean_options else None
            
            # Bean selection dropdown
            selected_bean_display = st.selectbox(
                "🌱 Select Green Beans",
                options=list(bean_options.keys()),
                index=0 if default_bean else None
            )
            
            # Get the selected bean ID and info
            if selected_bean_display:
                selected_bean_id = bean_options[selected_bean_display]
                selected_bean = next((bean for bean in green_beans if bean['bean_id'] == selected_bean_id), None)
                
                # Display info about the selected bean
                if selected_bean:
                    st.info(f"Selected: {selected_bean['name']} from {selected_bean['origin']}, "
                            f"Processing: {selected_bean['processing']}, "
                            f"Current stock: {selected_bean['current_stock_kg']}kg")
        else:
            st.warning("No green beans in inventory. Please add green beans first.")
            selected_bean_id = None
            selected_bean = None
        
        # Amount used for this roast
        amount_used_kg = st.number_input(
            "🏋️ Amount Used (kg)",
            min_value=0.1,
            max_value=float(selected_bean['current_stock_kg']) if selected_bean else 10.0,
            value=1.0,
            step=0.1
        )
        
        # Other roast form fields
        date = st.date_input("📅 Date")
        
        # Use the selected bean name if available
        coffee_name = st.text_input(
            "☕ Coffee Name", 
            value=selected_bean['name'] if selected_bean else ""
        )
        
        # Your existing roast parameters
        col1, col2 = st.columns(2)
        with col1:
            agtron_whole = st.number_input("🎯 Agtron Whole Bean", min_value=0, max_value=100, value=90)
            agtron_ground = st.number_input("🎯 Agtron Ground", min_value=0, max_value=100, value=95)
            drop_temp = st.number_input("🌡️ Drop Temperature (°C)", min_value=180.0, max_value=240.0, value=210.0, step=0.5)
        
        with col2:
            development_time = st.number_input("⏱️ Development Time (min)", min_value=0.0, max_value=5.0, value=1.0, step=0.01)
            total_time = st.number_input("⏱️ Total Time (min)", min_value=0.0, max_value=20.0, value=12.0, step=0.01)
            
            # Calculate DTR automatically
            if total_time > 0:
                dtr_ratio = development_time / total_time
            else:
                dtr_ratio = 0
            
            st.metric("DTR Ratio", f"{dtr_ratio:.2f}")
        
        notes = st.text_area("📝 Roast Notes")
        
        submit_button = st.form_submit_button("📝 Save Roast")
        
        if submit_button:
            if not selected_bean_id:
                st.error("Please select green beans from inventory!")
            elif not coffee_name:
                st.error("Coffee name is required!")
            elif selected_bean and amount_used_kg > selected_bean['current_stock_kg']:
                st.error(f"Not enough stock! Only {selected_bean['current_stock_kg']}kg available.")
            else:
                # Create roast record
                roast_data = {
                    "date": date.strftime("%Y-%m-%d"),
                    "coffee_name": coffee_name,
                    "agtron_whole": agtron_whole,
                    "agtron_ground": agtron_ground,
                    "drop_temp": drop_temp,
                    "development_time": development_time,
                    "total_time": total_time,
                    "dtr_ratio": dtr_ratio,
                    "notes": notes,
                    "bean_id": selected_bean_id  # Link to the green bean
                }
                
                # Save the roast
                result = api_call("/roasts/", method="post", data=roast_data)
                
                if result and "roast_id" in result:
                    # Update green bean stock
                    stock_update = api_call(
                        f"/green-beans/{selected_bean_id}/update-stock", 
                        method="put",
                        data={"amount_used": amount_used_kg}
                    )
                    
                    if stock_update:
                        st.success(f"Roast recorded successfully! Green bean stock updated to {stock_update.get('new_stock_kg', 0)}kg")
                    else:
                        st.warning("Roast recorded, but failed to update green bean stock.")
                else:
                    st.error("Error recording roast!")

def set_page(page):
    st.session_state.current_page = page