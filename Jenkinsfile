pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'prasadk0143/foodieverse'
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/prasad1057/FoodieVerse.git'

            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    echo $PASSWORD | docker login -u $USERNAME --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
            withEnv(["KUBECONFIG=/var/lib/jenkins/.kube/config"]) {
                 sh '''
                     kind load docker-image $DOCKER_IMAGE
                     kubectl apply -f k8s/deployment.yml
                     kubectl apply -f k8s/service.yml
                    '''

            }
        }
    }
}
