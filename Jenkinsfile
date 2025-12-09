pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "eu-north-1"
        ECR_REPO = "559938827680.dkr.ecr.eu-north-1.amazonaws.com/percy-blog"
        GITOPS_REPO = "https://github.com/Shakurrrr/gitops-blog-deploy.git"
        GITOPS_DIR = "gitops-blog-deploy/k8s"
    }

    stages {

        stage('Checkout App Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Shakurrrr/PERCY-BLOG-WEBSITE.git'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_KEY',
                    passwordVariable: 'AWS_SECRET'
                )]) {
                    sh '''
                        aws configure set aws_access_key_id $AWS_KEY
                        aws configure set aws_secret_access_key $AWS_SECRET
                        aws configure set default.region ${AWS_DEFAULT_REGION}

                        aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
                            docker login --username AWS --password-stdin ${ECR_REPO}
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = "v${BUILD_NUMBER}"
                }

                sh '''
                    docker build \
                      --platform linux/amd64 \
                      -t ${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Update GitOps Repo') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GH_USER',
                    passwordVariable: 'GH_TOKEN'
                )]) {
                    sh '''
                        rm -rf gitops-blog-deploy
                        git clone https://${GH_USER}:${GH_TOKEN}@github.com/Shakurrrr/gitops-blog-deploy.git

                        sed -i "s|image:.*|image: ${ECR_REPO}:${IMAGE_TAG}|" \
                            ${GITOPS_DIR}/deployment.yaml

                        cd gitops-blog-deploy
                        git config user.email "jenkins@ci.com"
                        git config user.name "Jenkins CI"

                        git add .
                        git commit -m "Deploy ${IMAGE_TAG}" || echo "No changes to commit"
                        git push
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🚀 GitOps update complete → ArgoCD syncing → EKS deploying."
        }
        failure {
            echo "❌ Build failed. Check console output."
        }
    }
}
