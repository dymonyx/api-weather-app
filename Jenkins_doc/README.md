## Setting up Jenkins on a Virtual Machine and Integrating with GitLab
This document explains how to set up Jenkins on a virtual machine, configure credentials, create a pipeline, integrate it with GitLab, and provides examples of successful and failed jobs.

### Installing Jenkins on a Virtual Machine
#### Step 1: Update System and Install Java 17
`sudo apt update`

`sudo apt install -y openjdk-17-jdk`

#### Step 2: Add Jenkins Repository and Install Jenkins
```
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```
`sudo apt-get update`

`sudo apt-get install jenkins`

#### Step 3: Check Jenkins service status and get the initial admin password
`sudo systemctl status jenkins`

### Configuring Credentials in Jenkins
Jenkins Dashboard → Manage Jenkins → Manage Credentials → Global credentials.
Add dockerhub credential.

![img1](img/image1.png)

### Creating a Jenkins Pipeline and Integrating with GitLab
Jenkins Dashboard → Click New Item → Multibranch Pipeline. Name pipeline (e.g., api-weather), and click OK.

![img2](img/image2.png)

Conncet to your GitLab project URL (create some tokens).

![img3](img/image3.png)

### Add Jenkinsfile to your project
Jenkinsfile can be like this:
```
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

```
### Example of a Successful Job
Stage view.

![img4](img/image4.png)

Successful Job has mark ✅.

![img5](img/image5.png)

Pipeline overview. Successful Job passed all the stages.

![img6](img/image6.png)
### Example of an Unstable Job
Unstable job - one of stage fell but it's only unstable status. Also we have artifact archive.

![img7](img/image7.png)

Stage view.

![img8](img/image8.png)
### Example of a Failed Job
Stage Docker Push fell because of invalid command.

![img9](img/image9.png)
### Jenkins Plugins
Manage Jenkins → Plugins.

Gitlab Branch Source.

![img10](img/image10.png)

Pipeline: Stage View.

![img11](img/image11.png)
### Gitlab
Gitlab integration with Jenkins.

![img12](img/image12.png)

### Helpful Links
- [dockerhub image agoneek/api-weather](https://hub.docker.com/r/agoneek/api-weather/tags)
- [building with docker using Jenkins](https://www.liatrio.com/resources/blog/building-with-docker-using-jenkins-pipelines)
- [linting dockerfiles in Jenkins](https://itobey.dev/linting-dockerfiles-in-jenkins-pipelines-with-hadolint/)
- [hadolint integration in Jenkins](https://github.com/hadolint/hadolint/blob/master/docs/INTEGRATION.md)
- [currentBuild description in Jenkins](https://stackoverflow.com/questions/43639099/set-the-build-name-and-description-from-a-jenkins-declarative-pipeline)