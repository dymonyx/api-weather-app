node {
    stage('Dockerfile Lint') {
        def hadolintResult = sh(
            script: 'docker run --rm -v $(pwd):/mnt hadolint/hadolint:latest-debian hadolint /mnt/* | tee -a hadolint_lint.txt',
            returnStatus: true
        )
        if (hadolintResult != 0) {
            currentBuild.result = 'UNSTABLE'
            archiveArtifacts artifacts: 'hadolint_lint.txt', allowEmptyArchive: true
        }
    }

    stage('Dockerfile Build') {
        sh 'docker build -t agoneek/api-weather:latest .'
    }

    stage('Dockerfile Push') {
        withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
            sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
            sh 'docker push agoneek/api-weather:latest'
            sh 'docker logout'
        }
    }
    stage('Dockerfile Pull') {
        sh 'docker image pull agoneek/api-weather:latest'
    }
}
