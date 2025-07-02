pipeline {
    agent any

    environment {
        IMAGE_NAME = 'prasadk0143/foodieverse'
    }

    stages {
        

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}")
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
        stage('Deploy to k8s'){
            steps{
                script{
                    sh 'kubectl apply -f deployment.yml'
                    sh 'kubectl apply -f service.yml'
                }
            }
        }
                stage('Deploy to Kubernetes') {
            steps {
                sh '''
                cat <<EOF | kubectl apply -f -
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                  name: foodieverse
                spec:
                  replicas: 1
                  selector:
                    matchLabels:
                      app: foodieverse
                  template:
                    metadata:
                      labels:
                        app: foodieverse
                    spec:
                      containers:
                      - name: foodieverse
                        image: $DOCKER_IMAGE
                        ports:
                        - containerPort: 5000
                ---
                apiVersion: v1
                kind: Service
                metadata:
                  name: foodieverse-service
                spec:
                  type: NodePort
                  selector:
                    app: foodieverse
                  ports:
                  - protocol: TCP
                    port: 80
                    targetPort: 5000
                    nodePort: 30036
                EOF
                '''
            }
        }
    }
}

    
