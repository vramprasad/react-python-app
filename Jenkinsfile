pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_TAG = "${BUILD_NUMBER}"
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
            steps {
                sh '''
                    docker image ls
                    echo $IMAGE_TAG
                '''
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