pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('docker-creds')
    }

    stages {
        stage('build') {
            steps {
                echo 'building docker image'
                sh 'docker build -t ltmr/legacy-airline-system .'
            }
        }

        stage('login to docker hub') {
            steps {
                echo 'logging into docker hub'
                sh "echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin"
            }
        }

        stage('push image') {
            steps {
                echo 'pushing docker image to hub'
                sh 'docker push ltmr/legacy-airline-system'
            }
        }
    }
}
