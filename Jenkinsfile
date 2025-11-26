pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('ef6967c5-bfa5-48ad-a531-930eb9a5f9c4')
        IMAGE_NAME = "shehu98/percy-blog-website"
        ANSIBLE_INVENTORY = "/home/shakur/ansible-deployments/inventory.ini"
        ANSIBLE_PLAYBOOK = "/home/shakur/ansible-deployments/deploy-blog.yaml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Cloning the GitHub repository..."
                git branch: 'main', url: 'https://github.com/Shakurrrr/PERCY-BLOG-WEBSITE.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh '''
                    docker build -t $IMAGE_NAME:${BUILD_NUMBER} .
                    docker tag $IMAGE_NAME:${BUILD_NUMBER} $IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                echo "🔐 Logging into DockerHub..."
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "🚀 Pushing Docker image to DockerHub..."
                sh '''
                    docker push $IMAGE_NAME:${BUILD_NUMBER}
                    docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                echo "⚙️ Deploying Percy Blog via Ansible..."
                sshagent(['ansible_ssh_key']) {
                    sh '''
                        ansible-playbook -i $ANSIBLE_INVENTORY $ANSIBLE_PLAYBOOK \
                        --become --become-user=root --become-method=sudo
                    '''
                    echo "✅ Deployment successful!"
                }
            }
        }

        stage('Clean Workspace') {
            steps {
                echo "🧹 Cleaning workspace..."
                cleanWs()
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully! Image built, pushed, and deployed."
        }
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
    }
}
