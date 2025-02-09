# Use the official Apache Airflow image
FROM apache/airflow:2.7.2

# Set working directory
WORKDIR /opt/airflow

# Copy the requirements file
COPY requirements_streamlit.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the correct user is used
USER airflow

# Set entrypoint
ENTRYPOINT ["/entrypoint"]
