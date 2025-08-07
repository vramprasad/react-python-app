pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_BUILDKIT = '1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Images') {
            parallel {
                stage('Build Backend') {
                    steps {
                        script {
                            dir('backend') {
                                sh '''
                                    docker build -t ${DOCKER_REGISTRY}/myapp-backend:${IMAGE_TAG} .
                                    docker build -t ${DOCKER_REGISTRY}/myapp-backend:latest .
                                '''
                            }
                        }
                    }
                }
                stage('Build Frontend') {
                    steps {
                        script {
                            dir('frontend') {
                                sh '''
                                    docker build -t ${DOCKER_REGISTRY}/myapp-frontend:${IMAGE_TAG} .
                                    docker build -t ${DOCKER_REGISTRY}/myapp-frontend:latest .
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        script {
                            sh '''
                                docker run --rm ${DOCKER_REGISTRY}/myapp-backend:${IMAGE_TAG} \
                                python -m pytest tests/ -v
                            '''
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        script {
                            sh '''
                                docker run --rm ${DOCKER_REGISTRY}/myapp-frontend:${IMAGE_TAG} \
                                npm test -- --coverage --watchAll=false
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh '''
                        # Scan images for vulnerabilities
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_REGISTRY}/myapp-backend:${IMAGE_TAG}
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_REGISTRY}/myapp-frontend:${IMAGE_TAG}
                    '''
                }
            }
        }
        
        stage('Push Images') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-registry-creds', 
                                                    passwordVariable: 'DOCKER_PASSWORD', 
                                                    usernameVariable: 'DOCKER_USERNAME')]) {
                        sh '''
                            echo $DOCKER_PASSWORD | docker login ${DOCKER_REGISTRY} -u $DOCKER_USERNAME --password-stdin
                            docker push ${DOCKER_REGISTRY}/myapp-backend:${IMAGE_TAG}
                            docker push ${DOCKER_REGISTRY}/myapp-backend:latest
                            docker push ${DOCKER_REGISTRY}/myapp-frontend:${IMAGE_TAG}
                            docker push ${DOCKER_REGISTRY}/myapp-frontend:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        # Update docker-compose.yml with new image tags
                        sed -i "s/myapp-backend:latest/myapp-backend:${IMAGE_TAG}/g" docker-compose.prod.yml
                        sed -i "s/myapp-frontend:latest/myapp-frontend:${IMAGE_TAG}/g" docker-compose.prod.yml
                        
                        # Deploy using docker-compose
                        docker-compose -f docker-compose.prod.yml up -d --force-recreate
                        
                        # Wait for services to be healthy
                        sleep 30
                        
                        # Verify deployment
                        docker-compose -f docker-compose.prod.yml ps
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Clean up
            sh '''
                docker system prune -f
                docker image prune -f
            '''
        }
        success {
            echo 'Pipeline succeeded!'
            // Add notifications here (Slack, email, etc.)
        }
        failure {
            echo 'Pipeline failed!'
            // Add failure notifications here
        }
    }
}