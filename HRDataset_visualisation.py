import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the dataset from the CSV file
data = pd.read_csv('/content/HRDataset_v14.csv')

# Bar Chart of Employee Count by Gender
# Count the number of employees by gender
gender_counts = data['Sex'].value_counts()

# Create a bar chart
plt.bar(gender_counts.index, gender_counts.values)

# Add labels and title
plt.xlabel('Gender')
plt.ylabel('Number of Employees')
plt.title('Employee Count by Gender')

# Show the plot
plt.show()

# Pie Chart of Marital Status Distribution
# Count the number of employees in each marital status
marital_status_counts = data['MaritalDesc'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))  
plt.pie(marital_status_counts, labels=marital_status_counts.index, autopct='%1.1f%%', startangle=140)

# Add a title
plt.title('Marital Status Distribution')

# Show the plot
plt.show()

# Histogram of Employee Ages
# Function to calculate age from DOB
def calculate_age(dob_str):
# Try to parse the date with '/' separator and 4-digit year first
    try:
        dob = datetime.strptime(dob_str, '%m/%d/%Y')
    except ValueError:
        # If it fails, try with '-' separator and 4-digit year
        try:
            dob = datetime.strptime(dob_str, '%m-%d-%Y')
        except ValueError:
            # If it fails again, try with '/' separator and 2-digit year
            dob = datetime.strptime(dob_str, '%m/%d/%y')
        
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # Ensure that the calculated age is not negative
    if age < 0:
        age = abs(age)

    return age

# Calculate ages for all employees in the dataset
data['Age'] = data['DOB'].apply(lambda dob_str: calculate_age(dob_str))

# Create a histogram
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
plt.hist(data['Age'], bins=20, edgecolor='k', alpha=0.7)

# Add labels and title
plt.xlabel('Age')
plt.ylabel('Number of Employees')
plt.title('Histogram of Employee Ages')

# Show the plot
plt.tight_layout()
plt.show()

# Box Plot of Salary Distribution
# Create a box plot of salary distribution within each department
plt.figure(figsize=(12, 6))  # Adjust the figure size if needed
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.title('Salary Distribution by Department')

# Use Matplotlib's boxplot function
plt.boxplot([data[data['Department'] == dept]['Salary'] for dept in data['Department'].unique()],
        labels=data['Department'].unique())

# Add labels
plt.xlabel('Department')
plt.ylabel('Salary')

# Show the plot
plt.tight_layout()
plt.show()

# Stacked Bar Chart of Employment Status by Gender
# Group data by Employment Status and Sex and count the number of employees
employment_status_gender_counts = data.groupby(['EmploymentStatus', 'Sex']).size().unstack(fill_value=0)

# Create a stacked bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
employment_status_gender_counts.plot(kind='bar', stacked=True)

# Add labels and title
plt.xlabel('Employment Status')
plt.ylabel('Number of Employees')
plt.title('Stacked Bar Chart of Employment Status by Gender')

# Add a legend
plt.legend(title='Sex')

# Show the plot
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()
plt.show()

# Scatter Plot of Engagement Survey vs. Employee Satisfaction
# Extract data for the X and Y axes
engagement_survey_scores = data['EngagementSurvey']
employee_satisfaction_scores = data['EmpSatisfaction']

# Create a scatter plot
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
plt.scatter(engagement_survey_scores, employee_satisfaction_scores, alpha=0.5)

# Add labels and title
plt.xlabel('Engagement Survey Score')
plt.ylabel('Employee Satisfaction Score')
plt.title('Scatter Plot of Engagement Survey vs. Employee Satisfaction')

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()

# Line Chart of Absences Over Time
# Convert 'DateofHire' to datetime objects with flexible parsing (replace invalid dates with NaT)
data['DateofHire'] = pd.to_datetime(data['DateofHire'], format="%m/%d/%Y", errors='coerce')

# Drop rows with missing or invalid dates (NaT)
data.dropna(subset=['DateofHire'], inplace=True)

# Group data by 'DateofHire' and count the number of absences
absences_over_time = data.groupby('DateofHire')['Absences'].sum()

# Create a line chart
plt.figure(figsize=(12, 6))  # Adjust the figure size if needed
plt.plot(absences_over_time.index, absences_over_time.values, marker='o', linestyle='-')

# Add labels and title
plt.xlabel('Date of Hire')
plt.ylabel('Number of Absences')
plt.title('Line Chart of Absences Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()

# Bar Chart of Employee Count by Department
# Group data by 'Department' and count the number of employees in each department
department_employee_counts = data['Department'].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
department_employee_counts.plot(kind='bar', color='skyblue')

# Add labels and title
plt.xlabel('Department')
plt.ylabel('Number of Employees')
plt.title('Bar Chart of Employee Count by Department')

# Show the plot
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()
plt.show()

# Stacked Bar Chart of Termination Reasons by Department
# Filter rows where Termd is True (indicating termination) and group by 'Department' and 'TermReason'
termination_data = data[data['Termd'] == 1].groupby(['Department', 'TermReason']).size().unstack(fill_value=0)

# Create a stacked bar chart
plt.figure(figsize=(12, 6))  # Adjust the figure size if needed
termination_data.plot(kind='bar', stacked=True)

# Add labels and title
plt.xlabel('Department')
plt.ylabel('Number of Terminations')
plt.title('Stacked Bar Chart of Termination Reasons by Department')

# Add a legend
plt.legend(title='Termination Reason', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()
plt.show()

# Heatmap of Correlation Matrix
# Select numeric columns for the correlation matrix
numeric_columns = data.select_dtypes(include=['float64', 'int64'])

# Calculate the correlation matrix
correlation_matrix = numeric_columns.corr()

# Create a heatmap
plt.figure(figsize=(12, 8))  # Adjust the figure size if needed
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)

# Add title
plt.title('Heatmap of Correlation Matrix')

# Show the plot
plt.tight_layout()
plt.show()