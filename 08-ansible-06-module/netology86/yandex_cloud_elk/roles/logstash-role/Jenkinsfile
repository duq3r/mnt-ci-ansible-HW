pipeline {
    agent {
        label 'docker'
    }
    stages {
//         stage('Checkout') {
//             steps{
//                 git branch: 'main', credentialsId: '0b54df1a-ee4b-40da-b8bb-a70fcf46e73f', url: 'git@github.com:run0ut/logstash-role.git'
//             }
//         }
        stage('Install molecule') {
            steps{
                sh 'pip3 install -r test-requirements.txt'
                sh "echo =============="
            }
        }
        stage('Run Molecule'){
            steps{
                sh 'molecule test'
                // Clean workspace after testing
                cleanWs()
            }
        }
    }
}
