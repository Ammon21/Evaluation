import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Function to plot the radar chart with world-class aesthetics
def plot_radar_chart(teacher_data, teacher_name, feature_columns):
    # Calculate the average of the columns for the selected teacher
    values = teacher_data[feature_columns].mean().tolist()

    # Create radar chart
    fig = go.Figure()

    # Adding the radar chart
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=feature_columns,
        fill='toself',
        name=teacher_name,
        text=feature_columns,  # Tooltip text on hover
        hoverinfo='text+name+r',  # Display name and value on hover
        line=dict(
            color='rgba(255, 165, 0, 0.8)',  # Creamy orange line
            width=3,
            dash='solid',  # Solid line for a sleek look
        ),
        marker=dict(
            size=10,
            color='rgba(255, 165, 0, 0.9)',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=2),
        ),
        fillcolor='rgba(255, 165, 0, 0.3)',  # Semi-transparent orange fill
    ))

    # Adding a gradient background for the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],  # Assuming the rating is from 0 to 5
                tickvals=[0, 1, 2, 3, 4, 5],  # Radial ticks
                ticktext=['0', '1', '2', '3', '4', '5'],  # Radial ticks text
                tickfont=dict(size=14, color='rgba(200, 200, 200, 0.8)'),  # Radial tick font size
            ),
            angularaxis=dict(
                visible=False,  # Hide the angular axis labels (column names)
            ),
        ),
        title=f"Teacher Evaluation for {teacher_name}",
        title_font=dict(
            size=24,
            color='rgb(44, 62, 80)',
            family="Arial, sans-serif",
            weight='bold',
        ),
        font=dict(size=16, color='rgb(44, 62, 80)', family="Arial, sans-serif"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background for the plot area
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background for the chart
        showlegend=True,
        margin=dict(t=40, b=40, l=40, r=40),
        hovermode="closest",  # Closest hover effect
        xaxis=dict(showgrid=False),  # Hiding gridlines for a clean look
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(200, 200, 200, 0.3)'),
        hoverlabel=dict(bgcolor='rgba(255, 165, 0, 0.8)', font_size=16, font_family="Arial, sans-serif"),
        dragmode='zoom',  # Zoom effect for interactivity
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
            .card {
                padding: 15px;
                margin: 15px 0;
                border-radius: 10px;
                box-shadow: 0px 12px 18px rgba(0, 0, 0, 0.15);
                font-size: 16px;
                color: #2c3e50;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .strength-card {
                background: linear-gradient(145deg, #28a745, #218838);
                color: white;
            }
            .weakness-card {
                background: linear-gradient(145deg, #dc3545, #c82333);
                color: white;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0px 18px 24px rgba(0, 0, 0, 0.2);
            }
            .card-header {
                font-size: 18px;
                font-weight: bold;
                color: #fff;
                display: flex;
                align-items: center;
            }
            .card-content {
                font-size: 16px;
            }
            .card-icon {
                font-size: 28px;
                margin-right: 10px;
            }
            .strength {
                color: #28a745;
            }
            .weakness {
                color: #dc3545;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
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
    st.plotly_chart(radar_chart)

    # Calculate Strength and Weakness
    # Strength: Three columns with the highest average score
    strength_columns = average_scores.nlargest(3).index.tolist()
    strength_scores = average_scores.nlargest(3).tolist()

    # Weakness: Three columns with the lowest average score
    weakness_columns = average_scores.nsmallest(3).index.tolist()
    weakness_scores = average_scores.nsmallest(3).tolist()

    # Display Strengths and Weaknesses
    st.subheader("Strengths Based on Students Perspective")
    st.markdown('<div class="container">', unsafe_allow_html=True)
    for col, score in zip(strength_columns, strength_scores):
        st.markdown(f"""
            <div class="card strength-card">
                <div class="card-header">
                    <span class="card-icon">👍</span> Strength
                </div>
                <div class="card-content">
                    {col}: {score:.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Weaknesses Based on Students Perspective")
    st.markdown('<div class="container">', unsafe_allow_html=True)
    for col, score in zip(weakness_columns, weakness_scores):
        st.markdown(f"""
            <div class="card weakness-card">
                <div class="card-header">
                    <span class="card-icon">👎</span> Weakness
                </div>
                <div class="card-content">
                    {col}: {score:.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
