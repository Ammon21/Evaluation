import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Function to plot the ultimate radar chart with a world-class design
def plot_radar_chart(teacher_data, teacher_name, feature_columns):
    # Calculate the average of the columns for the selected teacher
    values = teacher_data[feature_columns].mean().tolist()

    # Create radar chart with a top-tier design
    fig = go.Figure()

    # Adding the radar chart with a clean, minimalistic design
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=feature_columns,
        fill='toself',
        name=teacher_name,
        text=feature_columns,  # Tooltip text on hover
        hoverinfo='text+name+r',  # Display name and value on hover
        line=dict(
            color='rgba(93, 164, 214, 0.9)',  # Elegant blue with gradient effect
            width=4,
            dash='solid',  # Clean, solid line for professional feel
        ),
        marker=dict(
            size=12,
            color='rgba(93, 164, 214, 1)',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=3),
        ),
        fillcolor='rgba(93, 164, 214, 0.5)',  # Subtle fill for modern look
    ))

    # Adding a premium gradient background for the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],  # Assuming the rating is from 0 to 5
                tickvals=[0, 1, 2, 3, 4, 5],  # Radial ticks
                ticktext=['0', '1', '2', '3', '4', '5'],  # Radial ticks text
                tickfont=dict(size=14, color='rgb(200, 200, 200)'),  # Radial tick font size
            ),
            angularaxis=dict(
                visible=False,  # Removing angular axis labels (column names)
            ),
        ),
        title=f"Teacher Evaluation for {teacher_name}",
        title_font=dict(
            size=24, 
            color='rgb(44, 62, 80)', 
            family="Arial, sans-serif", 
            weight='bold'
        ),
        font=dict(size=14, color='rgb(44, 62, 80)', family="Arial, sans-serif"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background for the plot area
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background for the chart
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50),
        hovermode="closest",  # Closest hover effect
    )

    # Adding a subtle glowing effect on hover for a futuristic look
    fig.update_traces(
        hovertemplate="<b>%{theta}</b><br>Score: %{r}<extra></extra>",
        hoverlabel=dict(bgcolor='rgba(44, 62, 80, 0.8)', font_size=15, font_family="Arial", font_color='white'),
    )

    return fig

# Main Streamlit function
def radar_dashboard():
    st.title("Teachers Evaluation Dashboard")

    # Stylish header
    st.markdown("""
        <style>
            body {
                background-color: #f4f4f9;
                font-family: 'Helvetica Neue', sans-serif;
                margin: 0;
            }
            .header {
                font-size: 28px;
                color: #2c3e50;
                font-weight: 700;
                text-align: center;
                margin-top: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Load the dataset from CSV
    df = pd.read_csv('eval.csv', encoding='cp1252')

    # Teacher selection dropdown
    teacher_list = df['Teacher'].unique()
    teacher_to_analyze = st.selectbox('Select a Teacher', teacher_list, key="teacher_select")

    # Filter the dataset for the selected teacher
    teacher_data = df[df['Teacher'] == teacher_to_analyze]

    # Assuming the features in the dataset start from the second column onwards, excluding 'Teacher', 'Section', 'Grade'
    feature_columns = [col for col in df.columns if col not in ['Teacher', 'Section', 'Grade']]  # Exclude these columns

    # Calculate the average score for each feature for the selected teacher
    average_scores = teacher_data[feature_columns].mean()

    # Generate radar chart
    radar_chart = plot_radar_chart(teacher_data, teacher_to_analyze, feature_columns)

    # Show the radar chart in Streamlit
    st.plotly_chart(radar_chart, use_container_width=True)

    # Calculate Strength and Weakness
    # Strength: Three columns with the highest average score
    strength_columns = average_scores.nlargest(3).index.tolist()
    strength_scores = average_scores.nlargest(3).tolist()

    # Weakness: Three columns with the lowest average score
    weakness_columns = average_scores.nsmallest(3).index.tolist()
    weakness_scores = average_scores.nsmallest(3).tolist()

    # Display Strengths and Weaknesses in a visually appealing manner
    st.subheader("Strengths Based on Students Perspective")
    for col, score in zip(strength_columns, strength_scores):
        st.markdown(f"""
            <div style="padding: 10px; margin: 10px 0; border-radius: 10px; background: linear-gradient(145deg, #28a745, #218838); color: white; display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 10px;">👍</span>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{col}</div>
                    <div>{score:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("Weaknesses Based on Students Perspective")
    for col, score in zip(weakness_columns, weakness_scores):
        st.markdown(f"""
            <div style="padding: 10px; margin: 10px 0; border-radius: 10px; background: linear-gradient(145deg, #dc3545, #c82333); color: white; display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 10px;">👎</span>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{col}</div>
                    <div>{score:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
