def sourceEnvironment = ["dc25_qaautocand", "dc25_qacand", "dc25_qademouxr", "dc25_qavies", "dc25_qavdemosac", "dc25_qacandies"]
def target_environment = ["dc25_qaautocand", "dc25_qacand", "dc25_qademouxr", "dc25_qavies", "dc25_qavdemosac", "dc25_qacandies"]
def targetPoolID = ["dbPool1"]

pipeline {
    options {
        ansiColor('xterm')
    }
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml"""
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: sfhcm-jenkins-tools.docker.repositories.sapcdn.io/jnlp-alpine:4.3.4-sap-01
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
  - name: sf-k8s-python
    image: sfhcm.docker.repositories.sap.ondemand.com/sf-k8s/tools/python:3.9-slim-buster
    imagePullPolicy: Always
    command: ['cat']
    tty: true
  - name: docker
    image: sfhcm-jenkins-tools.docker.repositories.sapcdn.io/docker:19.03
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
"""
        }
    }

    parameters {
        choice(name: 'SourceEnvironment', choices: sourceEnvironment, description: 'Data taken from the Environment.')
        choice(name: 'Target_environment', choices: target_environment, description: 'Environment to be copied.')
        string(name: 'sourceCompanyID', defaultValue: '', description: 'Company ID name') 
        string(name: 'targetCompanyId', defaultValue: '', description: 'Target company ID name')
        string(name: 'targetCompanyName', defaultValue: '', description: 'Target company name to be')
        choice(name: 'targetPoolID', defaultValue: '', description: 'Target DB pool name either dbPool1 or dbPool2')
    }

    environment {
        SRCENV_NAME = "${params.SourceEnvironment}"
        SRC_ID = "${params.sourceCompanyID}"
        TRGENV_NAME = "${params.Target_environment}"
        TRG_ID = "${params.targetCompanyId}"
        TRG_CNAME = "${params.targetCompanyName}"
        TRGDB_POOL = "${params.targetPoolID}"
    }

    stages {
        stage("GIT Checkout") {
            steps {
                script {
                    dir('companycopydc25') {
                        git credentialsId: 'sf-prod-config-self-service-serviceuser',
                        url: "${}", branch: 'main'
                    }
                }
            }
        }
        
        stage("company-clone") {
            steps {
                script {
                    container("sf-k8s-python") {
                        withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                            dir("companycopydc25") {
                                sh "python3 ImportTest.py ${SRCENV_NAME} ${SRC_ID} ${TRGENV_NAME} ${TRG_ID} ${TRG_CNAME} ${TRGDB_POOL}"
                            }
                        }
                    }
                }
            }
        }
        
    }
}
