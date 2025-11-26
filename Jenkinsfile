pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('ef6967c5-bfa5-48ad-a531-930eb9a5f9c4')
        IMAGE_NAME       = "shehu98/percy-blog-website"
        TAG              = "${BUILD_NUMBER}"
        INVENTORY_FILE   = "/home/shakur/ansible-deployments/inventory.ini"
        PLAYBOOK_FILE    = "/home/shakur/ansible-deployments/deploy-blog.yaml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Pulling GitHub repository..."
                git branch: 'main', url: 'https://github.com/Shakurrrr/PERCY-BLOG-WEBSITE.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh '''
                    docker build -t $IMAGE_NAME:$TAG .
                    docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                echo "🔐 Logging into DockerHub..."
                sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login \
                    -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "🚀 Pushing Docker images..."
                sh '''
                    docker push $IMAGE_NAME:$TAG
                    docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                echo "⚙️ Running Ansible deployment..."
                sshagent(['ansible_ssh_key']) {
                    sh '''
                        ansible-playbook -i $INVENTORY_FILE $PLAYBOOK_FILE \
                        --extra-vars "image_tag=$TAG" \
                        --become --become-user=root --become-method=sudo
                    '''
                }
                echo "✨ Deployment completed!"
            }
        }

        stage('Cleanup') {
            steps {
                echo "🧹 Cleaning Jenkins workspace..."
                cleanWs()
            }
        }
    }

    post {
        success {
            echo "🎉 SUCCESS: Build, push, and deployment completed!"
        }
        failure {
            echo "❌ FAILURE: Something went wrong. Check logs."
        }
    }
}
