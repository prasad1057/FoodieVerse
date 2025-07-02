pipeline {
    agent any

    environment {
        IMAGE_NAME = 'prasadk0143/foodieverse'
    }

    stages {
        

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${foodie}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                            dockerImage.push("latest")
                        }
                    }
                }
            }
        }
    }
}
