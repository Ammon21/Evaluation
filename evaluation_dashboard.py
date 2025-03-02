import streamlit as st
import pandas as pd
import plotly.graph_objects as go



def show_evaluation_dashboard():
    st.title("Lebawi international Academy")
# Load the dataset from CSV
    df = pd.read_csv('eval.csv', encoding='cp1252')  # Make sure the file 'eval.csv' is in the correct path

    # Create a stylish header for the academy name and logo
    st.markdown("""
        <style>ss
            /* General Styles */
            body {
                background-color: #f4f4f9;  /* Subtle off-white background */
                font-family: 'Helvetica Neue', sans-serif;
                margin: 0;
            }
            .header {
                font-size: 28px;  /* Smaller size for the header */
                color: #2c3e50;
                font-weight: 700;
                text-align: center;
                margin-top: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            /* Styling for dropdown menus with bold title */
            .dropdown-style label {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 8px;
            }

            .dropdown-style select {
                font-size: 16px;
                font-weight: bold;
                color: #34495e;
                border-radius: 8px;
                border: 2px solid #3498db;  /* Thin blue border */
                padding: 12px 18px;
                background-color: #ecf0f1;
                width: 100%;
                box-sizing: border-box;
                transition: all 0.3s ease;
                cursor: pointer;  /* Pointer cursor to mimic clickable dropdown */
            }
            .dropdown-style select:hover {
                border-color: #3498db;
                background-color: #e8f6fc;
            }
            .dropdown-style select:focus {
                outline: none;
                border-color: #8e44ad;
                box-shadow: 0px 0px 5px rgba(142, 68, 173, 0.6);
                background-color: #d3e9f9;
            }

            /* Circle Styling with Thinner Border and Smaller Text */
            .circle {
                border: 6px solid #3498db;  /* Thinner blue border */
                border-radius: 50%;         /* Circular shape */
                width: 200px;  /* Smaller circle */
                height: 200px;  /* Smaller circle */
                display: flex;
                justify-content: center;
                align-items: center;
                color: #2c3e50;
                font-size: 45px;  /* Smaller text inside */
                font-weight: 700;
                text-align: center;
                background-color: transparent; /* No fill color */
                margin: 20px auto;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);  /* Less shadow */
                position: relative;
                transition: all 0.3s ease;  /* Add transition for hover effect */
            }

            .circle .value {
                font-size: 40px;  /* Smaller number inside */
                color: #2c3e50;
                font-weight: 700;
            }

            .circle::before {
                content: '';
                position: absolute;
                width: 40px;
                height: 40px;
                background-color: #3498db;
                border-radius: 50%;
                top: 8px;
                right: 8px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }

            .circle:hover {
                cursor: pointer;
                border-color: #8e44ad;  /* Change border color on hover */
                box-shadow: 0px 8px 20px rgba(142, 68, 173, 0.3);  /* Add shadow on hover */
                transform: scale(1.05);  /* Slightly enlarge the circle on hover */
            }

            /* Separation Line */
            .separator {
                border-top: 2px solid #3498db;
                margin-top: 30px;
                margin-bottom: 30px;
            }

            /* Top Line Styling */
            .line-above {
                border-top: 3px solid #3498db;
                width: 100%;
                margin-bottom: 15px;
                background: linear-gradient(to right, #3498db, #8e44ad);  /* Gradient line */
                height: 3px;
            }

            /* Custom Table Styling */
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                border-radius: 8px;
                overflow: hidden;
            }
            th, td {
                padding: 12px 18px;
                text-align: center;
                border: 1px solid #ddd;
            }
            th {
                background-color: #3498db;
                color: white;
                font-size: 16px;
            }
            td {
                background-color: #ecf0f1;
                font-size: 14px;
            }
            tr:hover td {
                background-color: #d0e4f0;
            }

            /* Footer Styles */
            .footer {
                font-size: 14px;
                color: #7f8c8d;
                text-align: center;
                padding: 10px;
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #ffffff;
                box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1);
            }

            .footer a {
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display the academy name and logo in a row
    col1, col2 = st.columns([1, 3])  # First column for logo, second for the text

    with col1:
        # Display logo (adjust width as needed)
        st.image('logo.png', width=80)  # Logo resized smaller

    with col2:
        # Create a stylish header for the dashboard
        st.markdown('<div class="header">Teachers Evaluation Dashboard</div>', unsafe_allow_html=True)

    # Add a modern, colorful line above the "Teachers Evaluation Dashboard"
    st.markdown('<div class="line-above"></div>', unsafe_allow_html=True)

    # Separator line between the header and main content
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Dropdowns side by side (Teacher and Grade Filters)
    col1, col2 = st.columns(2)  # Create two columns for dropdowns

    with col1:
        teacher_list = df['Teacher'].unique()  # Assuming 'Teacher' is the column for teachers
        teacher_to_analyze = st.selectbox(
            'Select a Teacher',
            teacher_list,
            help="Choose a teacher to analyze their evaluation data.",
            key="teacher_select",
            format_func=lambda x: x.title()  # Capitalize the teacher name
        )

    with col2:
        # Dropdown to filter by Grade
        grade_filter = st.selectbox(
            'Select Grade to analyze',
            ['All Grades'] + list(df['Grade'].unique()),  # Using 'Grade' column
            help="Choose a grade to analyze teacher's performance in.",
            key="grade_select",
        )

    # Create an additional option for the "All Ratings" option, combining all columns
    column_to_analyze = st.selectbox(
        'Select a column to see its average by Grade',
        ['All Ratings'] + list(df.columns[3:]),  # Adding "All Ratings" as an option
        help="Select a column to display the average rating by grade.",
        key="column_select",
    )

    # Filter data based on the selected Teacher
    filtered_df = df[df['Teacher'] == teacher_to_analyze]

    # If 'All Grades' is selected, show the average for all grades
    if grade_filter == 'All Grades':
        if column_to_analyze == 'All Ratings':
            grouped = filtered_df.drop(columns=['Teacher']).groupby('Grade').mean().mean(axis=1)
            total_average = grouped.mean()  # Average of all grades
        else:
            grouped = filtered_df.groupby('Grade')[column_to_analyze].mean()
            total_average = grouped.mean()  # Average of all grades
    else:
        # Filter data based on selected Grade
        filtered_df = filtered_df[filtered_df['Grade'] == grade_filter]
        if column_to_analyze == 'All Ratings':
            grouped = filtered_df.drop(columns=['Teacher']).groupby('Grade').mean().mean(axis=1)
            total_average = grouped.mean()  # Average of the selected grade
        else:
            grouped = filtered_df.groupby('Grade')[column_to_analyze].mean()
            total_average = grouped.mean()  # Average of the selected grade

    # Layout with columns: One for the table and one for the circle
    col1, col2 = st.columns([2, 1])  # Create two columns: one for the table and one for the circle

    with col1:
        st.write(f"Average {column_to_analyze} by Grade for {teacher_to_analyze}:")
        st.markdown(f"""
            <table>
                <thead>
                    <tr>
                        <th>Grade</th>
                        <th>Average {column_to_analyze}</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'<tr><td>{grade}</td><td>{value:.2f}</td></tr>' for grade, value in grouped.items()])}
                </tbody>
            </table>
        """, unsafe_allow_html=True)

    with col2:
        # Create a visually appealing modern circle with no fill and a thinner blue border
        st.markdown(f"""
            <div class="circle">
                <div class="value">{total_average:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Display total average for the selected column and Teacher
    st.write(f"Total average of {column_to_analyze} for {teacher_to_analyze}: {total_average:.2f}")

    # Footer at the bottom with
    st.markdown("""
        <div class="footer">
            Designed by Ammon, Data Analyst, QA | 2025
        </div>
    """, unsafe_allow_html=True)
