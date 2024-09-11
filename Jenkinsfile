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
        stage('Initialize Python and needed Configs') {
            steps {
                sh """
                   exit 0
                """
                 }
         }
     }
 }
}
