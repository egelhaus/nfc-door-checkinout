pipeline {
    agent any

    stages {
            
        stage('Update System') {
            steps {
                sh """
                    apt update
                    apt upgrade -y
                    apt install python3
                    exit 0
                """
                  }
        }
        stage('Initialize Python and needed Configs') {
            steps {
                sh """
                   cp /root/.env
                   python3 -m venv venv
                   . venv/bin/activate
                   exit 0
                """
                 }
         }
        stage('Install or Update Python Packages') {
            steps {
                sh """
                   . venv/bin/activate
                   pip install flask python-dotenv mysqlclient mysql-connector-python
                   exit 0
                """
                 }
         }
        stage('Initialize Server') {
            steps {
                sh """
                  chmod +x run-server.sh
                  ./run-server.sh
                """
                 }
         }
     }
 }

