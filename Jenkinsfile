pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('ef6967c5-bfa5-48ad-a531-930eb9a5f9c4')
        IMAGE_NAME = "shehu98/percy-blog-website"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shakurrrr/PERCY-BLOG-WEBSITE.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:${BUILD_NUMBER} .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME:${BUILD_NUMBER}'
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully and image pushed to DockerHub!"
        }
        failure {
            echo "❌ Pipeline Failed. Check logs."
        }
    }
}
