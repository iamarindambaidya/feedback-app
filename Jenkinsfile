pipeline {
    agent any

    environment {
        DOCKER_API_IMAGE = "dockerforuser/feedback-api:latest"
        DOCKER_FE_IMAGE = "dockerforuser/feedback-frontend:latest"
    }

    stages {
        stage('Build Docker Images') {
            steps {
                sh 'docker build -t $DOCKER_API_IMAGE ./api'
                sh 'docker build -t $DOCKER_FE_IMAGE ./frontend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_API_IMAGE
                        docker push $DOCKER_FE_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-jenkins', variable: 'KUBECONFIG')]) {
                    sh '''
                        export KUBECONFIG=/home/ubuntu/.kube/config
                        kubectl apply --validate=false -f k8s/
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD pipeline successful!"
        }
        failure {
            echo "❌ CI/CD pipeline failed!"
        }
    }
}
