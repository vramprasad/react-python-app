pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_TAG = "1." + "${BUILD_NUMBER}"
        DOCKER_BUILDKIT = '1'
    }
    
    // Start of stages
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            parallel {
                stage('Build Backend') {
                    steps {
                        script {
                            dir('backend') {
                                sh '''
                                    docker build -t ${DOCKER_REGISTRY}/backend:${IMAGE_TAG} .
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
                                    docker build -t ${DOCKER_REGISTRY}/frontend:${IMAGE_TAG} .
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        
    }
    // End of stages

    post {
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