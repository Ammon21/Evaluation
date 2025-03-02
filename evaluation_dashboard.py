import streamlit as st
import pandas as pd

def show_evaluation_dashboard():
    st.title("Lebawi International Academy")

    # Load the dataset from CSV
    df = pd.read_csv('eval.csv', encoding='cp1252')  # Make sure the file 'eval.csv' is in the correct path

    # Create a stylish header for the academy name and logo
    st.markdown("""
        <style>
            /* General Styles */
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
                border: 2px solid #3498db;
                padding: 12px 18px;
                background-color: #ecf0f1;
                width: 100%;
                box-sizing: border-box;
                transition: all 0.3s ease;
                cursor: pointer;
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

            /* Circle Styling */
            .circle {
                border: 6px solid #3498db;
                border-radius: 50%;
                width: 200px;
                height: 200px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #2c3e50;
                font-size: 45px;
                font-weight: 700;
                text-align: center;
                background-color: transparent;
                margin: 20px auto;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                position: relative;
                transition: all 0.3s ease;
            }

            .circle .value {
                font-size: 40px;
                color: #2c3e50;
                font-weight: 700;
            }

            .circle:hover {
                cursor: pointer;
                border-color: #8e44ad;
                box-shadow: 0px 8px 20px rgba(142, 68, 173, 0.3);
                transform: scale(1.05);
            }

            .separator {
                border-top: 2px solid #3498db;
                margin-top: 30px;
                margin-bottom: 30px;
            }

            .line-above {
                border-top: 3px solid #3498db;
                width: 100%;
                margin-bottom: 15px;
                background: linear-gradient(to right, #3498db, #8e44ad);
                height: 3px;
            }

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

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image('logo.png', width=80)

    with col2:
        st.markdown('<div class="header">Teachers Evaluation Dashboard</div>', unsafe_allow_html=True)

    st.markdown('<div class="line-above"></div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        teacher_list = df['Teacher'].unique()
        teacher_to_analyze = st.selectbox(
            'Select a Teacher',
            teacher_list,
            help="Choose a teacher to analyze their evaluation data.",
            key="teacher_select",
            format_func=lambda x: x.title()
        )

    with col2:
        grade_filter = st.selectbox(
            'Select Grade to analyze',
            ['All Grades'] + list(df['Grade'].unique()),
            help="Choose a grade to analyze teacher's performance in.",
            key="grade_select",
        )

    column_to_analyze = st.selectbox(
        'Select a column to see its average by Grade',
        ['All Ratings'] + list(df.columns[3:]),
        help="Select a column to display the average rating by grade.",
        key="column_select",
    )

    filtered_df = df[df['Teacher'] == teacher_to_analyze]

    if grade_filter == 'All Grades':
        if column_to_analyze == 'All Ratings':
            grouped = filtered_df.drop(columns=['Teacher']).groupby('Grade').mean().mean(axis=1)
            total_average = grouped.mean() if not grouped.empty else 0
        else:
            grouped = filtered_df.groupby('Grade')[column_to_analyze].mean()
            total_average = grouped.mean() if not grouped.empty else 0
    else:
        filtered_df = filtered_df[filtered_df['Grade'] == grade_filter]
        if column_to_analyze == 'All Ratings':
            grouped = filtered_df.drop(columns=['Teacher']).groupby('Grade').mean().mean(axis=1)
            total_average = grouped.mean() if not grouped.empty else 0
        else:
            grouped = filtered_df.groupby('Grade')[column_to_analyze].mean()
            total_average = grouped.mean() if not grouped.empty else 0

    col1, col2 = st.columns([2, 1])

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
        st.markdown(f"""
            <div class="circle">
                <div class="value">{total_average:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write(f"Total average of {column_to_analyze} for {teacher_to_analyze}: {total_average:.2f}")

    st.markdown("""
        <div class="footer">
            Designed by Ammon, Data Analyst, QA | 2025
        </div>
    """, unsafe_allow_html=True)
