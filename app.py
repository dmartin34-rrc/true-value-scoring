import streamlit as st
import pandas as pd
import plotly.express as px

# App Config & Styling
st.set_page_config(page_title="The Stat-Pad Index", layout="wide")

st.markdown("""
    <style>
        h1 { border-bottom: 2px solid #60A5FA; padding-bottom: 10px; }
        .insight-box {
            background-color: rgba(96, 165, 250, 0.1);
            border-left: 5px solid #60A5FA;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("True Value Scoring")

# Key Insight Narrative
st.markdown("""
    <div class="insight-box">
        Total points don't always tell the whole story. By breaking down scoring by <strong>Game Margin</strong>, this dashboard reveals exactly how many points were scored in crucial, close-game situations versus low-pressure garbage time.
    </div>
""", unsafe_allow_html=True)

# Historical Data
player_profiles = [
    {"id": "Bam Adebayo (83)", "date": "Mar 10, 2026", "stats": [(0, 0), (11, 8), (38, 20), (34, 15)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/mia.png", "url": "https://www.youtube.com/watch?v=AfHhcjfalgs"},
    {"id": "Kobe Bryant (81)", "date": "Jan 22, 2006", "stats": [(45, 24), (20, 10), (16, 8), (0, 0)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/lal.png", "url": "https://www.youtube.com/watch?v=m3Zu-GIprUY"},
    {"id": "Luka Doncic (73)", "date": "Jan 26, 2024", "stats": [(20, 12), (30, 18), (23, 15), (0, 0)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png", "url": "https://www.youtube.com/watch?v=zW9-9tSd2Uk"},
    {"id": "Damian Lillard (71)", "date": "Feb 26, 2023", "stats": [(10, 8), (15, 10), (30, 16), (16, 5)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/por.png", "url": "https://www.youtube.com/watch?v=ipT37NfSkvM"},
    {"id": "Donovan Mitchell (71)", "date": "Jan 2, 2023", "stats": [(35, 22), (25, 18), (11, 10), (0, 0)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/cle.png", "url": "https://www.youtube.com/watch?v=ADDaeK8fQVw"},
    {"id": "Joel Embiid (70)", "date": "Jan 22, 2024", "stats": [(15, 10), (10, 8), (35, 18), (10, 2)], "team_logo": "https://a.espncdn.com/i/teamlogos/nba/500/phi.png", "url": "https://www.youtube.com/watch?v=IyoJXJqkPpE"}
]

categories = ["1. Trailing (Down 1+)", "2. Clutch (Tied to Up 5)", "3. Comfortable (Up 6-14)", "4. Garbage Time (Up 15+)"]

# Build the Dataset
data = []
for player in player_profiles:
    total_mins = sum(mins for pts, mins in player["stats"])
    
    for category, (pts, mins) in zip(categories, player["stats"]):
        data.append({
            "Performance": player["id"], 
            "Date": player["date"],
            "Total_Minutes": total_mins,
            "Game Margin": category, 
            "Points Scored": pts, 
            "Minutes": mins,
            "PPM": round(pts / mins, 2) if mins > 0 else 0,
            "Bar Label": f"{pts} pts<br>({mins}m)" if pts > 0 else "",
            "URL": player["url"],
            "Logo": player["team_logo"]
        })

df = pd.DataFrame(data)

# Sort the dataframe so the highest total points are at the top
df['Total Points'] = df.groupby('Performance')['Points Scored'].transform('sum')
df = df.sort_values(by=['Total Points', 'Performance'], ascending=[True, False])

# Bar Chart
fig = px.bar(
    df, y="Performance", x="Points Scored", color="Game Margin", orientation='h',
    text="Bar Label", custom_data=['Minutes', 'PPM'],
    color_discrete_map={
        "1. Trailing (Down 1+)": "#E63946",       
        "2. Clutch (Tied to Up 5)": "#F4A261",    
        "3. Comfortable (Up 6-14)": "#457B9D",    
        "4. Garbage Time (Up 15+)": "#2B2D42"     
    }
)

fig.update_traces(
    textposition='inside', 
    textfont=dict(size=13, color='white', family="Arial Black"),
    marker_line_color='rgba(0,0,0,0.5)', marker_line_width=2,
    hovertemplate="<b>%{x} Points</b><br>Time Spent: %{customdata[0]} Minutes<br>Rate: %{customdata[1]} Pts/Min<extra></extra>"
)

# Labels & Logos
unique_profiles = df.drop_duplicates(subset=['Performance']).sort_values(by='Total Points', ascending=False)

tick_texts = [
    f"<a href='{row.URL}' target='_blank' style='color: #60A5FA; font-weight: bold; text-decoration: none;'>{row.Performance}</a><br>"
    f"<span style='color: gray; font-size: 12px;'>{row.Date}, {row.Total_Minutes} Min. played</span>"
    for row in unique_profiles.itertuples(index=False)
]

chart_images = [
    dict(
        source=row.Logo, xref="paper", yref="y", x=-0.01, y=row.Performance,          
        sizex=0.06, sizey=0.75, xanchor="right", yanchor="middle", layer="above"
    )
    for row in unique_profiles.itertuples(index=False)
]

fig.update_layout(
    barmode='stack', height=650, 
    margin=dict(t=80, b=60, l=220, r=40),
    images=chart_images,                  
    xaxis=dict(title="", showgrid=True, gridcolor="rgba(128, 128, 128, 0.2)"),
    yaxis=dict(title="", tickmode="array", tickvals=unique_profiles['Performance'], ticktext=tick_texts, ticklabelstandoff=70),
    legend=dict(title="", orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.38, font=dict(size=14)),
    annotations=[
        dict(
            text="Total Points Accumulated", x=0.38, y=-0.12, 
            xref="paper", yref="paper", showarrow=False, font=dict(size=16)
        )
    ],
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")
