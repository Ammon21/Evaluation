import streamlit as st
import pandas as pd

def show_evaluation_dashboard():
    st.title("Lebawi International Academy")

    # Load the dataset from CSV
    df = pd.read_csv('eval.csv', encoding='cp1252')

    # Create a stylish header
    st.markdown("""
        <style>
            .header { font-size: 28px; color: #2c3e50; font-weight: 700; text-align: center; }
            .circle { border: 6px solid #3498db; border-radius: 50%; width: 150px; height: 150px;
                      display: flex; justify-content: center; align-items: center;
                      color: #2c3e50; font-size: 35px; font-weight: 700; margin: 20px auto; }
            .footer { font-size: 14px; color: #7f8c8d; text-align: center; margin-top: 20px; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image('logo.png', width=80)
    with col2:
        st.markdown('<div class="header">Teachers Evaluation Dashboard</div>', unsafe_allow_html=True)

    teacher_list = df['Teacher'].unique()
    teacher_to_analyze = st.selectbox('Select a Teacher', teacher_list, key="teacher_select")

    grade_filter = st.selectbox('Select Grade to analyze', ['All Grades'] + list(df['Grade'].unique()), key="grade_select")

    column_to_analyze = st.selectbox('Select a column to see its average by Grade',
                                     ['All Ratings'] + list(df.columns[3:]), key="column_select")

    filtered_df = df[df['Teacher'] == teacher_to_analyze]
    numeric_columns = filtered_df.select_dtypes(include=['number']).columns

    if grade_filter == 'All Grades':
        if column_to_analyze == 'All Ratings':
            grouped = filtered_df[numeric_columns].groupby('Grade').mean().mean(axis=1)
        else:
            grouped = filtered_df.groupby('Grade')[column_to_analyze].mean()
        
        grade_counts = filtered_df['Grade'].value_counts()
        total_average = (grouped * grade_counts).sum() / grade_counts.sum() if not grouped.empty else 0
    else:
        filtered_df = filtered_df[filtered_df['Grade'] == grade_filter]
        if column_to_analyze == 'All Ratings':
            total_average = filtered_df[numeric_columns].mean().mean() if not filtered_df.empty else 0
        else:
            total_average = filtered_df[column_to_analyze].mean() if not filtered_df.empty else 0

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"Average {column_to_analyze} by Grade for {teacher_to_analyze}:")
        st.table(grouped.round(2))
    
    with col2:
        st.markdown(f"""
            <div class="circle">{total_average:.2f}</div>
        """, unsafe_allow_html=True)
    
    st.write(f"Total weighted average of {column_to_analyze} for {teacher_to_analyze}: {total_average:.2f}")

    st.markdown("""
        <div class="footer">Designed by Ammon | Data Analyst | Quality Assurance | 2025</div>
    """, unsafe_allow_html=True)