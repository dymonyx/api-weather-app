properties([
    parameters([
        booleanParam(name: 'DEPLOY_TO_PROD', defaultValue: false, description: 'Do you want to deploy to prod?')
    ])
])


node {
    stage('Checkout') {
        checkout scm
    }
    // stage('Dockerfile Lint') {
    //     sh 'docker run --rm -v $(pwd):/mnt hadolint/hadolint:latest-debian hadolint /mnt/Dockerfile | tee hadolint_lint.txt'
    //     int hadolintResult = sh(script: 'test -s hadolint_lint.txt', returnStatus: true)
    //     if (hadolintResult == 0) {
    //         currentBuild.result = 'UNSTABLE'
    //         archiveArtifacts artifacts: 'hadolint_lint.txt', allowEmptyArchive: true
    //     }
    // }
    // stage('Dockerfile Build') {
    //     sh 'docker build -t agoneek/api-weather:latest .'
    // }
    // stage('Dockerfile Push') {
    //     withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
    //         sh(script: '''
    //             echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    //             docker push agoneek/api-weather:latest
    //             docker logout
    //             rm /var/lib/jenkins/.docker/config.json
    //         ''', returnStatus: true)
    //     }
    //     script {
    //         currentBuild.displayName = 'api-weather/agoneek Dockerfile.'
    //         currentBuild.description = 'Link of image in DockerHub: <br> ' +
    //         "<a href='https://hub.docker.com/r/agoneek/api-weather' target='_blank'>" +
    //         'DockerHub: agoneek/api-weather</a><br>' +
    //         'Command for pulling latest image: <br> ' +
    //         '<code>docker pull agoneek/api-weather:latest</code>'
    //     }
    // }
    // stage('Deploy to Dev') {
    //     withCredentials([string(credentialsId: 'KUBECONFIG_BASE64', variable: 'KUBE_B64')]) {
    //         sh '''
    //             echo "$KUBE_B64" | base64 -d > kubeconfig
    //             export KUBECONFIG=$(pwd)/kubeconfig
    //             kubectl apply -n dev -f k8s_deploy/dev/api-weather-deployment.yml
    //             kubectl rollout restart deployment api-weather-deployment -n dev
    //             kubectl rollout status deployment api-weather-deployment -n dev
    //             kubectl apply -n dev -f k8s_deploy/dev/service.yml
    //             kubectl apply -n ingress-nginx -f k8s_deploy/dev/ingress-nginx.yml
    //             kubectl apply -n metallb-system -f k8s_deploy/dev/metalb-config.yml
    //             rm kubeconfig
    //         '''
    //     }
    // }
    // stage('Smoke test (dev)') {
    //     String url = 'http://dev.dymonyx.ru/info'
    //     String result = sh(script: "curl -s ${url} | jq -r '.service'", returnStdout: true).trim()
    //     if (result != 'weather') {
    //         error "Dev test failed: expected 'weather', got '${result}'"
    //     }
    // }
    // stage('Get Weather Test (dev)') {
    //     String url = 'http://dev.dymonyx.ru/info/weather?city=Saint-Petersburg&date_from=2024-02-19&date_to=2024-02-20'
    //     String result = sh(script:"curl -s ${url} | jq", returnStdout: true).trim()

    //     String expected = '''
    //         {
    //         "service": "weather",
    //         "data": {
    //             "temperature_c": {
    //             "average": -4.12,
    //             "median": -3,
    //             "min": -11,
    //             "max": -0.9
    //             }
    //         }
    //         }
    //         '''
    //     if (result != expected.trim()) {
    //         error "Dev API answer doesn\'t match with Saint-P answer"
    //     }
    // }
    // stage('Deploy to Prod') {
    //     if (params.DEPLOY_TO_PROD) {
    //         withCredentials([string(credentialsId: 'KUBECONFIG_BASE64', variable: 'KUBE_B64')]) {
    //             sh '''
    //                 echo "$KUBE_B64" | base64 -d > kubeconfig
    //                 export KUBECONFIG=$(pwd)/kubeconfig
    //                 kubectl apply -n default -f k8s_deploy/default/api-weather-deployment.yml
    //                 kubectl rollout restart deployment api-weather-deployment -n default
    //                 kubectl rollout status deployment api-weather-deployment -n default
    //                 kubectl apply -n default -f k8s_deploy/default/service.yml
    //                 kubectl apply -n ingress-nginx -f k8s_deploy/default/ingress-nginx.yml
    //                 kubectl apply -n metallb-system -f k8s_deploy/default/metalb-config.yml
    //                 rm kubeconfig
    //             '''
    //         }
    //     }
    // }
    stage('Smoke test (prod)') {
        if (params.DEPLOY_TO_PROD) {
            sh 'hostname'
            String url = 'http://www.dymonyx.ru/info'
            String result = sh(script: "curl -s ${url} | jq -r '.service'", returnStdout: true).trim()
            echo "Got response: '${result}'"
            if (result != 'weather') {
                error "Prod test failed: expected 'weather', got '${result}'"
            }
        }
    }
    stage('Get Weather Test (prod)') {
        if (params.DEPLOY_TO_PROD) {
            sh 'hostname'
            String url = 'http://www.dymonyx.ru/info/weather?city=Saint-Petersburg&date_from=2024-02-19&date_to=2024-02-20'
            String result = sh(script:"curl -s ${url} | jq", returnStdout: true).trim()
            echo "Got response: '${result}'"
            String expected = '''
                {
                "service": "weather",
                "data": {
                    "temperature_c": {
                    "average": -4.12,
                    "median": -3,
                    "min": -11,
                    "max": -0.9
                    }
                }
                }
                '''
            if (result != expected.trim()) {
                error "Prod API answer doesn\'t match with Saint-P answer"
            }
        }
    }
}

