import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Set page config
st.set_page_config(page_title="Melbourne Housing Dashboard", layout="wide")

#Navigation Menu
page = st.radio(
    "🏠 Navigation",
    ['Home', 'About Us'],
    horizontal=True)
st.markdown("""***********************************************""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned melbourne housing.csv")
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Landsize'] = pd.to_numeric(df['Landsize'], errors='coerce')
    df['BuildingArea'] = pd.to_numeric(df['BuildingArea'], errors='coerce')
    df = df.dropna(subset=['Suburb', 'Price', 'Type', 'Rooms'])
    return df

df = load_data()
    
# Sidebar filters
st.sidebar.header("🔍 Filter Options")

suburbs = st.sidebar.multiselect(
    "Select Suburbs",
    options=sorted(df['Suburb'].unique()),
    default=sorted(df['Suburb'].unique())[:1]
)

types = st.sidebar.multiselect(
    "Select Property Types",
    options=sorted(df['Type'].unique()),
    default=sorted(df['Type'].unique())
)

min_rooms = st.sidebar.slider(
    "Minimum Rooms",
    min_value=int(df['Rooms'].min()),
    max_value=int(df['Rooms'].max()),
    value=2
)


 #Filter dataset
filtered_df = df[
    (df['Suburb'].isin(suburbs)) &
    (df['Type'].isin(types)) &
    (df['Rooms'] >= min_rooms) 
]  


# Home Page
if page == "Home":
    #Title and info
    st.image(gamba.jpg,width=300)
    st.markdown("""
    <h1 style='color: #2c3e50;'>🏘 Melbourne Property Listings</h1>
    <p style='color: #95a5a6;'>Visualize, filter and understand Melbourne's housing data.</p>
""", unsafe_allow_html=True)

    st.subheader("""Welcome! Find your ideal home here!""") 
    st.markdown("""Use the filter on the left to narrow down listings. Below you will see an overview of the listings and their price distributions""")
    st.markdown("""house type :""")
    st.markdown(""" h - house,villa,terrace""")
    st.markdown(""" u - duplex""")
    st.markdown(""" t - townhouse""")
    st.markdown("""***********************************************""")

# Inject CSS to change background
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5f5;
        }
        </style>
        """,
        unsafe_allow_html=True
)


#Dynamic stats
    st.markdown(f"**Showing** {len(filtered_df)} listing based on your filter.")
    col1, col2 = st.columns(2)
    col1.metric("Average Price", f"${int(filtered_df['Price'].mean()):,}" if not filtered_df.empty else "N/A")
    col2.metric("Max Price", f"${int(filtered_df['Price'].max()):,}" if not filtered_df.empty else "N/A")

    filtered_df['Price'] = filtered_df['Price'].apply(lambda x: f"${int(x):,}")

# Show filtered data
    st.dataframe(
        filtered_df[['Suburb', 'CouncilArea' , 'Address', 'Price', 'Type', 'Rooms','Landsize','BuildingArea']].sort_values(by='Price', ascending=False),
        use_container_width=True
    )


# Histogram
    st.subheader("Unit Availability")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(filtered_df['Suburb'], bins=40, color='skyblue', edgecolor='black')
    ax.set_title('Unit Available')
    ax.set_xlabel('Suburb')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Scatter plot
    st.subheader("💰 Price Distribution Across Selected Suburbs")
    
    scatter_df = df[['Price', 'Suburb']].dropna()
    scatter_df = scatter_df[scatter_df['Suburb'].isin(suburbs)]
   
    
    fig = px.strip(
        scatter_df,
        x='Suburb',
        y='Price',
        hover_data=['Suburb'],
        labels={'Price': 'Price (AUD)', 'Suburb': 'Suburb'},
        stripmode='overlay'
    )
    
    fig.update_layout(yaxis_tickformat="$,.0f")
    fig.update_traces(marker=dict(opacity=0.5, size=8, color='teal'))

    st.plotly_chart(fig, use_container_width=True)

    st.write(f"Total points plotted: {len(scatter_df)}")

# Optional: download button
st.sidebar.download_button(
    label="⬇️ Download Listing Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_melbourne_housing.csv',
    mime='text/csv'
)
#About Us Page
if page == "About Us":
    # Inject CSS to change background
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5f5;
        }
        </style>
        """,
        unsafe_allow_html=True
)
    st.subheader("About This Dashboard")
    st.markdown("""
    This app is built with **Streamlit** to analyze Melbourne housing data.

    **Features:**
    - Interactive filters for suburb and property type
    - Histogram of price distributions
    - Dynamic table of listings
    - Navigation bar and styled layout

    **Data Source:** Cleaned version of Melbourne housing dataset
    """)
    st.markdown("""Created by :""")
    st.markdown(""" Shah Jehan & Qawiem Lutfan""")
    
