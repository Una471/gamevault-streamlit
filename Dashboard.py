import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import base64 # Import the base64 module

# --- 1. Set Page Config (must be first Streamlit command) ---
# Set layout to wide and initial sidebar state to expanded for better visibility of filters.
st.set_page_config(layout="wide", page_title="2027 Dashboard - Expanded Business", initial_sidebar_state="expanded")

# --- Function to get base64 image for local files ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: Logo image not found at {image_path}. Please check the path.")
        return None # Return None if file not found

# --- Define your local logo path ---
your_local_logo_path = "C:/Users/PC/Downloads/Compressed/Unaswis_GameVault_Sept2027/logo.png"
logo_base64 = get_base64_image(your_local_logo_path)

# --- 2. Custom CSS Styling (Refined Dark Theme) ---
# This section applies custom CSS to style the Streamlit app for a truly dark, cohesive, and beautiful theme.
# It uses a deep dark background, soft contrasting text colors, and consistent styling for KPIs and plots.
st.markdown("""
    <style>
        /* General body and app container styling for a deep, modern dark theme */
        .main, .block-container, .stApp {
            background-color: #121212 !important; /* Very dark charcoal/almost black */
            color: #E0E0E0 !important; /* Soft white for general text, gentle on eyes */
        }
        /* Headings (h1-h6) colors */
        h1, h2, h3, h4, h5, h6 {
            color: #F0F0F0 !important; /* Bright white for headings for strong emphasis */
        }
        /* Styling for Streamlit Metric cards (KPIs) */
        .stMetric {
            background-color: #1F1F1F !important; /* Slightly lighter than main background for cards */
            border-radius: 16px; /* Modern rounded corners */
            padding: 25px; /* Ample padding inside cards */
            color: #E0E0E0 !important; /* Text color for cards */
            box-shadow: 8px 8px 20px rgba(0,0,0,0.7) !important; /* Stronger, diffused shadow for more attraction */
            margin-bottom: 25px; /* Increased space between metric cards */
            display: flex; /* Use flexbox for layout */
            flex-direction: column; /* Stack label and value vertically */
            align-items: flex-start; /* Align content to the start */
            height: 100%; /* Ensure all cards have similar height */
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; /* Smooth hover effects */
            border: 1px solid rgba(70,70,70,0.5); /* More visible subtle border for definition */
        }
        .stMetric:hover {
            transform: translateY(-8px); /* Lift effect on hover */
            box-shadow: 12px 12px 30px rgba(0,0,0,0.9) !important; /* Enhanced shadow on hover */
        }
        /* Style for the label part of the st.metric (e.g., "Total Revenue") */
        .stMetric > div:first-child {
            font-size: 1.4em !important; /* Optimized font size for labels */
            font-weight: 600 !important; /* Semi-bold for labels */
            color: #BB86FC !important; /* Vibrant but dark-friendly purple for labels for a premium feel */
            margin-bottom: 12px; /* More space between label and value */
            display: flex; /* Enable flex for icon and text */
            align-items: center; /* Vertically align icon and text */
        }
        /* Style for the value part of the st.metric (e.g., "P10,000.00") */
        .stMetric > div:last-child {
            font-size: 3.0em !important; /* Large, prominent font for values */
            font-weight: 700 !important; /* Bold font for KPI values */
            color: #FFFFFF !important; /* Pure white for values for maximum pop and readability */
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5); /* More pronounced text shadow for values */
        }
        /* Styling for Streamlit DataFrames and Tables */
        .stDataFrame, .stTable {
            background-color: #1F1F1F !important; /* Match card background for tables */
            color: #E0E0E0 !important; /* Light text for tables */
            border-radius: 12px; /* Rounded corners for tables */
        }
        /* Styling for Plotly toolbar (modebar) */
        .modebar {
            background-color: transparent !important; /* Transparent background for toolbar */
            color: #BB86FC !important; /* Purple for Plotly toolbar icons to match theme */
        }
        /* Styling for Plotly charts container */
        .stPlotlyChart {
            border-radius: 16px; /* Match KPI card rounded corners */
            overflow: hidden; /* Ensures content stays within rounded corners */
            background-color: #1F1F1F !important; /* Match card background for plots */
            padding: 20px; /* Consistent padding around the plot */
            box-shadow: 8px 8px 20px rgba(0,0,0,0.7) !important; /* Stronger shadow for plots */
            border: 1px solid rgba(70,70,70,0.5); /* More visible subtle border for definition */
            margin-bottom: 25px; /* Space between charts and sections */
        }
        /* Removed specific background colors for each KPI card as per request to make them all the same color */

        /* Icon styling for KPI cards - larger and with a subtle glow */
        .stMetric > div:first-child .icon {
            margin-right: 15px; /* Space between icon and text */
            font-size: 2.2em !important; /* Even larger icon for strong visual impact */
            line-height: 1; /* Ensure icon aligns well with text */
            text-shadow: 0px 0px 10px rgba(187,134,252,0.8); /* Glow matching label color */
        }

        /* Sidebar styling */
        .st-emotion-cache-vk3ypu { /* This targets the sidebar container */
            background-color: #4B0082 !important; /* Deep purple for sidebar background */
            padding: 25px; /* Increased padding */
            border-radius: 16px; /* Consistent rounded corners */
            box-shadow: 5px 0px 20px rgba(0,0,0,0.7);
        }
        .st-emotion-cache-vk3ypu h2 { /* Sidebar header */
            color: #FFFFFF !important; /* Bright white for sidebar header */
            font-size: 1.5em !important; /* Increased font size for sidebar header */
        }
        .st-emotion-cache-vk3ypu label { /* Sidebar labels for selectbox/date input */
            color: #E0E0E0 !important; /* Light text for labels */
            font-weight: bold;
            font-size: 1.1em !important; /* Increased font size for sidebar labels */
        }
        .st-emotion-cache-vk3ypu .stSelectbox > div > div { /* Selectbox background */
            background-color: #6A0DAD !important; /* Slightly lighter purple for input fields */
            color: #E0E0E0 !important;
            border-radius: 10px;
            border: 1px solid #BB86FC; /* Subtle purple border matching labels */
        }
        .st-emotion-cache-vk3ypu .stDateInput > div > div { /* Date input background */
            background-color: #6A0DAD !important;
            color: #E0E0E0 !important;
            border-radius: 10px;
            border: 1px solid #BB86FC; /* Subtle purple border matching labels */
        }
        .st-emotion-cache-vk3ypu .stDateInput input { /* Date input text color */
            color: #E0E0E0 !important;
        }
        /* Further refined styling for the plot titles and axes */
        .js-plotly-plot .plotly .main-svg .gtitle {
            fill: #F0F0F0 !important; /* Ensure Plotly titles use the heading color */
            font-size: 1.8em !important; /* Larger font size for plot titles */
            font-weight: 600 !important;
        }
        .js-plotly-plot .plotly .main-svg .g-xtick .xtick text,
        .js-plotly-plot .plotly .main-svg .g-ytick .ytick text,
        .js-plotly-plot .plotly .main-svg .g-zaxis .g-ztick .ztick text {
            fill: #FFFFFF !important; /* Ensure Plotly tick labels are pure white */
            font-size: 1.2em !important; /* Increased font size for tick labels */
        }
        .js-plotly-plot .plotly .main-svg .g-xaxis .gtitle,
        .js-plotly-plot .plotly .main-svg .g-yaxis .gtitle,
        .js-plotly-plot .plotly .main-svg .g-zaxis .gtitle {
            fill: #FFFFFF !important; /* Ensure Plotly axis titles are pure white */
            font-size: 1.4em !important; /* Increased font size for axis titles */
            font-weight: 500 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Dashboard Header with Logo and Title ---
if logo_base64: # Only display if logo was successfully loaded
    st.markdown(f"""
        <div class="dashboard-header">
            <img src="data:image/png;base64,{logo_base64}" alt="Game Vault Logo">
            <h1>Game Vault - Expanded Business Dashboard (September 2027)</h1>
        </div>
    """, unsafe_allow_html=True)
else: # Fallback if logo not found
    st.title("Game Vault - Expanded Business Dashboard (September 2027)")


# --- 3. Data Loading ---
# Using st.cache_data to cache the data loading, improving performance
@st.cache_data
def load_data():
    # Adjusted paths assuming the script is run from the same directory as the CSV files
    base_path = ""
    visits = pd.read_csv(f"{base_path}Visits_2027.csv")
    snacks = pd.read_csv(f"{base_path}Snacks_2027.csv")
    tournaments = pd.read_csv(f"{base_path}Tournaments_2027.csv")
    table_football = pd.read_csv(f"{base_path}TableFootball_2027.csv")
    snooker = pd.read_csv(f"{base_path}Snooker_2027.csv")
    expenses = pd.read_csv(f"{base_path}Expenses_2027.csv")
    
    return visits, snacks, snooker, table_football, tournaments, expenses

# Load all the datasets
visits, snacks, snooker, table_football, tournaments, expenses = load_data()

# --- 4. Data Preprocessing & Feature Engineering ---

# --- visits Preprocessing ---
visits.rename(columns={'Start Time': 'Time', 'Name': 'Customer Name'}, inplace=True)
visits['Date'] = pd.to_datetime(visits['Date'])

def parse_time_robustly(time_str):
    if pd.isna(time_str): return None
    time_str = str(time_str).strip()
    formats = ['%I:%M:%S %p', '%H:%M:%S', '%I:%M %p', '%H:%M']
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    return None
visits['Time'] = visits['Time'].apply(parse_time_robustly)
visits['Hour'] = visits['Time'].apply(lambda x: x.hour if x else None)
visits['Day of Week'] = visits['Date'].dt.day_name()
visits['Month'] = visits['Date'].dt.month_name()

def get_time_of_day(hour):
    if hour is None: return None
    if 7 <= hour < 12: return 'Morning'
    elif 12 <= hour < 17: return 'Afternoon'
    else: return 'Evening'
visits['Time of Day Category'] = visits['Hour'].apply(get_time_of_day)

visits['Amount Paid (P)'] = pd.to_numeric(visits['Amount Paid (P)'], errors='coerce').fillna(0)
visits['Duration'] = pd.to_numeric(visits['Duration'], errors='coerce').fillna(0)
visits['Rating (1-5)'] = pd.to_numeric(visits['Rating (1-5)'], errors='coerce').fillna(0)


# --- snacks Preprocessing ---
snacks.rename(columns={'Snack Type': 'Snack', 'Unit Price': 'Price (P)', 'Total Price': 'Total_Snack_Sale'}, inplace=True)
snacks['Date'] = pd.to_datetime(snacks['Date'])
snacks['Price (P)'] = pd.to_numeric(snacks['Price (P)'], errors='coerce').fillna(0)
snacks['Quantity'] = pd.to_numeric(snacks['Quantity'], errors='coerce').fillna(0)


# --- snooker Preprocessing ---
snooker.rename(columns={'Amount Paid (P)': 'Amount (P)'}, inplace=True)
snooker['Date'] = pd.to_datetime(snooker['Date'])
snooker['Amount (P)'] = pd.to_numeric(snooker['Amount (P)'], errors='coerce').fillna(0)


# --- table_football Preprocessing ---
table_football.rename(columns={'Amount Paid (P)': 'Amount (P)'}, inplace=True)
table_football['Date'] = pd.to_datetime(table_football['Date'])
table_football['Amount (P)'] = pd.to_numeric(table_football['Amount (P)'], errors='coerce').fillna(0)


# --- tournaments Preprocessing ---
tournaments.rename(columns={'Entry Fee (P)': 'EntryFeePaid', 'Name': 'Participant Name'}, inplace=True)
tournaments['Date'] = pd.to_datetime(tournaments['Date'])
tournaments['EntryFeePaid'] = pd.to_numeric(tournaments['EntryFeePaid'], errors='coerce').fillna(0)

tournament_revenue_monthly = 2200

# --- expenses Preprocessing ---
expenses['Date'] = pd.to_datetime(expenses['Date'])
expenses['Amount (P)'] = pd.to_numeric(expenses['Amount (P)'], errors='coerce').fillna(0)

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
min_date = visits['Date'].min().date()
max_date = visits['Date'].max().date()

selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) == 2:
    start_date_filter = pd.to_datetime(selected_date_range[0])
    end_date_filter = pd.to_datetime(selected_date_range[1])
else:
    start_date_filter = pd.to_datetime(selected_date_range[0])
    end_date_filter = start_date_filter

visits_filtered = visits[(visits['Date'] >= start_date_filter) & (visits['Date'] <= end_date_filter)]
snacks_filtered = snacks[(snacks['Date'] >= start_date_filter) & (snacks['Date'] <= end_date_filter)]
snooker_filtered = snooker[(snooker['Date'] >= start_date_filter) & (snooker['Date'] <= end_date_filter)]
table_football_filtered = table_football[(table_football['Date'] >= start_date_filter) & (table_football['Date'] <= end_date_filter)]
tournaments_filtered = tournaments[(tournaments['Date'] >= start_date_filter) & (tournaments['Date'] <= end_date_filter)]
expenses_filtered = expenses[(expenses['Date'] >= start_date_filter) & (expenses['Date'] <= end_date_filter)]

all_games = ['All Games'] + sorted(visits['Game Played'].unique().tolist())
selected_game = st.sidebar.selectbox('Filter by Game Played', all_games)

if selected_game != 'All Games':
    visits_filtered = visits_filtered[visits_filtered['Game Played'] == selected_game]


# --- 5. KPI Calculations (using filtered data) ---

total_gameplay_revenue = visits_filtered['Amount Paid (P)'].sum()
total_snack_revenue = snacks_filtered['Total_Snack_Sale'].sum()
total_snooker_revenue = snooker_filtered['Amount (P)'].sum()
total_tablefootball_revenue = table_football_filtered['Amount (P)'].sum()

actual_tournament_days_in_filter = tournaments_filtered['Date'].nunique()
total_tournament_revenue = actual_tournament_days_in_filter * 1100

overall_total_revenue = total_gameplay_revenue + total_snack_revenue + total_snooker_revenue + total_tablefootball_revenue + total_tournament_revenue

total_expenses = expenses_filtered['Amount (P)'].sum()

net_profit = overall_total_revenue - total_expenses
profit_margin = (net_profit / overall_total_revenue * 100) if overall_total_revenue != 0 else 0

total_visits_count = visits_filtered.shape[0]
unique_customers = visits_filtered['CustomerID'].nunique()
average_visit_duration = visits_filtered['Duration'].mean() if not visits_filtered.empty else 0

most_popular_game = visits_filtered['Game Played'].mode()[0] if not visits_filtered.empty else "N/A"

if not snacks_filtered.empty:
    most_popular_snack_by_qty = snacks_filtered.groupby('Snack')['Quantity'].sum().idxmax()
else:
    most_popular_snack_by_qty = "N/A"

average_rating = visits_filtered['Rating (1-5)'].mean() if not visits_filtered.empty else 0


# --- 6. Dashboard Layout and Visualizations ---

st.subheader("Key Performance Indicators")

def kpi_card(column, label, value, icon, css_class=""):
    with column:
        st.markdown(f"""
            <div class="stMetric {css_class}">
                <div><span class="icon">{icon}</span> {label}</div>
                <div>{value}</div>
            </div>
        """, unsafe_allow_html=True)

# Layout KPI cards using Streamlit columns
# All KPI cards will now have the same background color as defined in .stMetric CSS.
col1, col2, col3, col4, col5 = st.columns(5)
col6, col7, col8, col9, col10 = st.columns(5)

kpi_card(col1, "Net Profit", f"P{net_profit:,.2f}", "💸")
kpi_card(col2, "Gameplay Revenue", f"P{total_gameplay_revenue:,.2f}", "🎮")
kpi_card(col3, "Snack Revenue", f"P{total_snack_revenue:,.2f}", "🍔")
kpi_card(col4, "Total Visits", f"{total_visits_count:,}", "🚶")
kpi_card(col5, "Unique Customers", f"{unique_customers:,}", "🧑‍🤝‍🧑")

kpi_card(col6, "Tournament Revenue", f"P{total_tournament_revenue:,.2f}", "🏆")
kpi_card(col7, "Snooker Revenue", f"P{total_snooker_revenue:,.2f}", "🎱")
kpi_card(col8, "Table Football Revenue", f"P{total_tablefootball_revenue:,.2f}", "⚽")
kpi_card(col9, "Total Expenses", f"P{total_expenses:,.2f}", "📉")
kpi_card(col10, "Avg. Visit Duration", f"{average_visit_duration:.0f} mins", "⏱️")


st.markdown("---")

st.subheader("Core Business Insights")

# Arrange the next four core charts into a 2x2 grid for compact layout
col_row1_1, col_row1_2 = st.columns(2)
col_row2_1, col_row2_2 = st.columns(2)


with col_row1_1:
    # Most Played Games bar chart
    game_counts = visits_filtered['Game Played'].value_counts().reset_index(name='Count')
    game_counts.rename(columns={'index': 'Game Played'}, inplace=True)

    popular_games_fig = px.bar(
        game_counts,
        x='Game Played',
        y='Count',
        title='Most Played Games',
        labels={'Game Played': 'Game Played', 'Count': 'Number of Plays'},
        color_discrete_sequence=px.colors.sequential.Plasma_r, # Muted, dark-friendly sequential palette
        height=380 # Fixed height to control scrolling
    )
    popular_games_fig.update_layout(
        plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', # Match KPI card background
        font=dict(color='#FFFFFF', size=12), # All text white
        title_font_color='#FFFFFF', # White title
        xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14), # Increased font sizes
        yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14) # Increased font sizes
    )
    st.plotly_chart(popular_games_fig, use_container_width=True)

with col_row1_2:
    # Top Customers by Spending bar chart
    if not visits_filtered.empty:
        top_customers = visits_filtered.groupby('Customer Name')['Amount Paid (P)'].sum().nlargest(10).reset_index()
        top_customers_fig = px.bar(
            top_customers,
            x='Amount Paid (P)',
            y='Customer Name',
            orientation='h',
            title='Top Customers by Spending',
            labels={'Amount Paid (P)': 'Total Amount Paid (P)', 'Customer Name': 'Customer Name'},
            color_discrete_sequence=px.colors.sequential.Aggrnyl, # Another dark-friendly sequential palette
            height=380 # Fixed height
        )
        top_customers_fig.update_layout(
            plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', # Match KPI card background
            font=dict(color='#FFFFFF', size=12), # All text white
            title_font_color='#FFFFFF', # White title
            xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14), # Increased font sizes
            yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', autorange="reversed", title_font_size=18, tickfont_size=14) # Increased font sizes
        )
    else:
        top_customers_fig = go.Figure().add_annotation(x=0.5, y=0.5, text="No customer data available.", showarrow=False, font=dict(size=16, color='#E0E0E0'))
        top_customers_fig.update_layout(title_text="Top Customers by Spending", plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', font=dict(color='#E0E0E0'), title_font_color='#F0F0F0', height=380)
    st.plotly_chart(top_customers_fig, use_container_width=True)

with col_row2_1:
    # Expenses Breakdown pie chart
    expenses_breakdown_fig = px.pie(
        expenses_filtered,
        names='Expense Category',
        values='Amount (P)',
        title='Expenses by Category',
        hole=0.4, # Modern donut chart look
        color_discrete_sequence=px.colors.qualitative.D3, # D3 is generally dark-friendly and distinct
        height=380 # Fixed height
    )
    expenses_breakdown_fig.update_layout(
        plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', # Match KPI card background
        font=dict(color='#FFFFFF', size=12), # All text white
        title_font_color='#FFFFFF', # White title
        legend_font_color='#FFFFFF', # White legend text
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) # Move legend to top for space
    )
    st.plotly_chart(expenses_breakdown_fig, use_container_width=True)

with col_row2_2:
    # Snack Popularity bar chart
    if not snacks_filtered.empty:
        snack_popularity_fig = px.bar(
            snacks_filtered.groupby('Snack')['Quantity'].sum().reset_index(),
            x='Snack',
            y='Quantity',
            title='Snack Popularity',
            labels={'Quantity': 'Quantity Sold', 'Snack': 'Snack Type'},
            color_discrete_sequence=px.colors.sequential.OrRd, # Another appealing sequential palette
            height=380 # Fixed height
        )
        snack_popularity_fig.update_layout(
            plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', # Match KPI card background
            font=dict(color='#FFFFFF', size=12), # All text white
            title_font_color='#FFFFFF', # White title
            xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14),
            yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14)
        )
    else:
        snack_popularity_fig = go.Figure().add_annotation(x=0.5, y=0.5, text="No snack sales data available.", showarrow=False, font=dict(size=16, color='#E0E0E0'))
        snack_popularity_fig.update_layout(title_text="Snack Popularity", plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', font=dict(color='#E0E0E0'), title_font_color='#F0F0F0', height=380)
    st.plotly_chart(snack_popularity_fig, use_container_width=True)


st.markdown("---")

st.subheader("Revenue Trends & Customer Feedback")

# Arrange the last two charts into a 2-column layout to save vertical space
col_final1, col_final2 = st.columns(2)

with col_final1:
    # Revenue over Time line chart
    daily_gameplay_rev = visits_filtered.groupby('Date')['Amount Paid (P)'].sum().reset_index().rename(columns={'Amount Paid (P)': 'Gameplay Revenue'})
    daily_snack_rev = snacks_filtered.groupby('Date')['Total_Snack_Sale'].sum().reset_index().rename(columns={'Total_Snack_Sale': 'Snack Revenue'})
    daily_snooker_rev = snooker_filtered.groupby('Date')['Amount (P)'].sum().reset_index().rename(columns={'Amount (P)': 'Snooker Revenue'})
    daily_tablefootball_rev = table_football_filtered.groupby('Date')['Amount (P)'].sum().reset_index().rename(columns={'Amount (P)': 'Table Football Revenue'})

    daily_tournament_rev_df = pd.DataFrame({
        'Date': [pd.to_datetime('2027-09-25'), pd.to_datetime('2027-09-26')],
        'Tournament Revenue': [1100, 1100]
    })
    daily_tournament_rev_df_filtered = daily_tournament_rev_df[(daily_tournament_rev_df['Date'] >= start_date_filter) & (daily_tournament_rev_df['Date'] <= end_date_filter)]

    daily_revenue_combined = pd.merge(daily_gameplay_rev, daily_snack_rev, on='Date', how='outer').fillna(0)
    daily_revenue_combined = pd.merge(daily_revenue_combined, daily_snooker_rev, on='Date', how='outer').fillna(0)
    daily_revenue_combined = pd.merge(daily_revenue_combined, daily_tablefootball_rev, on='Date', how='outer').fillna(0)
    daily_revenue_combined = pd.merge(daily_revenue_combined, daily_tournament_rev_df_filtered, on='Date', how='outer').fillna(0)

    daily_revenue_combined['Total Daily Revenue'] = daily_revenue_combined['Gameplay Revenue'] + \
                                                      daily_revenue_combined['Snack Revenue'] + \
                                                      daily_revenue_combined['Snooker Revenue'] + \
                                                      daily_revenue_combined['Table Football Revenue'] + \
                                                      daily_revenue_combined['Tournament Revenue']

    revenue_over_time_fig = px.line(
        daily_revenue_combined.sort_values('Date'),
        x='Date',
        y='Gameplay Revenue',
        title='Daily Gameplay Revenue Trend',
        labels={'Gameplay Revenue': 'Amount (P)'},
        line_shape='linear',
        color_discrete_sequence=['#87CEEB'],
        height=380
    )
    revenue_over_time_fig.update_layout(
        plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F',
        font=dict(color='#FFFFFF', size=12),
        title_font_color='#FFFFFF',
        xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14),
        yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14)
    )
    st.plotly_chart(revenue_over_time_fig, use_container_width=True)

with col_final2:
    # Customer Rating Distribution bar chart
    if 'Rating (1-5)' in visits_filtered.columns and not visits_filtered['Rating (1-5)'].isnull().all():
        rating_counts = visits_filtered['Rating (1-5)'].value_counts().sort_index().reset_index(name='Count')
        rating_counts.rename(columns={'index': 'Rating (1-5)'}, inplace=True)

        fig_rate = px.bar(
            rating_counts,
            x='Rating (1-5)',
            y='Count',
            title='Customer Rating Distribution',
            labels={'Rating (1-5)': 'Rating (1-5)', 'Count': 'Number of Ratings'},
            color_discrete_sequence=['#F08080'],
            height=380
        )
        fig_rate.update_layout(
            xaxis_title="Rating (1-5)", yaxis_title="Count",
            plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F',
            font=dict(color='#FFFFFF', size=12),
            title_font_color='#FFFFFF',
            xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14),
            yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14)
        )
    else:
        fig_rate = go.Figure().add_annotation(x=0.5, y=0.5, text="No rating data available.", showarrow=False, font=dict(size=16, color='#E0E0E0'))
        fig_rate.update_layout(title_text="Customer Rating Distribution", plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F', font=dict(color='#E0E0E0'), title_font_color='#F0F0F0', height=380)
    st.plotly_chart(fig_rate, use_container_width=True)

# Age Distribution (moved to its own column in a new row for better layout, or could be combined with other insights)
st.markdown("---")
st.subheader("Customer Demographics")
# Place age distribution in a single column or combine with another if space allows.
# For now, keep it central, acknowledging it might still cause minimal scrolling if screen is small.
col_age = st.columns(1)[0]
with col_age:
    fig_age = px.histogram(
        visits_filtered,
        x='Age',
        nbins=10,
        title='Age Distribution',
        labels={'Age': 'Age', 'count': 'Number of Customers'},
        color_discrete_sequence=['#9370DB'],
        height=380
    )
    fig_age.update_layout(
        xaxis_title="Age", yaxis_title="Count",
        plot_bgcolor='#1F1F1F', paper_bgcolor='#1F1F1F',
        font=dict(color='#E0E0E0', size=12),
        title_font_color='#F0F0F0',
        xaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14),
        yaxis=dict(color='#FFFFFF', gridcolor='#3A3A3A', zerolinecolor='#3A3A3A', title_font_size=18, tickfont_size=14)
    )
    st.plotly_chart(fig_age, use_container_width=True)
