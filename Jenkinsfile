node {
    stage('Checkout') {
        checkout scm
    }
    stage('Dockerfile Lint') {
        sh 'docker run --rm -v $(pwd):/mnt hadolint/hadolint:latest-debian hadolint /mnt/Dockerfile | tee hadolint_lint.txt'
        def hadolintResult = sh(script: 'test -s hadolint_lint.txt', returnStatus: true)
        if (hadolintResult == 0) {
            currentBuild.result = 'UNSTABLE'
            archiveArtifacts artifacts: 'hadolint_lint.txt', allowEmptyArchive: true
        }
    }
    stage('Dockerfile Build') {
        sh 'docker build -t agoneek/api-weather:latest .'
    }
    stage('Dockerfile Push') {
        withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
            sh(script: '''
                echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                docker push agoneek/api-weather:latest
                docker logout
                rm /var/lib/jenkins/.docker/config.json
            ''', returnStatus: true)
        }
        script {
            currentBuild.displayName = 'api-weather/agoneek Dockerfile.'
            currentBuild.description = 'Link of image in DockerHub: <br> ' +
            "<a href='https://hub.docker.com/r/agoneek/api-weather' target='_blank'>" +
            'DockerHub: agoneek/api-weather</a><br>' +
            'Command for pulling latest image: <br> ' +
            '<code>docker pull agoneek/api-weather:latest</code>'
        }
    }
}
