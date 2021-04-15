def sourceEnvironment = ["dc25_qaautocand", "dc25_qacand", "dc25_qademouxr", "dc25_qavies", "dc25_qavdemosac", "dc25_qacandies"]
def target_environment = = ["dc25_qaautocand", "dc25_qacand", "dc25_qademouxr", "dc25_qavies", "dc25_qavdemosac", "dc25_qacandies"]
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
  - name: argocd
    image: sfhcm.docker.repositories.sap.ondemand.com/sf-k8s/tools/argocd-cli:v1.7.4
    command:
    - cat
    tty: true
  - name: curl
    image: sfhcm-jenkins-tools.docker.repositories.sapcdn.io/pstauffer/curl:v1.0.3
    command:
    - cat
    tty: true
  - name: yq
    image: sfhcm-jenkins-tools.docker.repositories.sapcdn.io/mikefarah/yq:3
    tty: true
  imagePullSecrets:
    - name: sfhcm-jenkins-tools-regcred
    - name: sfhcmartifactory
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
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
            environment {
                PROD_CONFIG_REPO = "${GITHUB_URL}${ORGANIZATION_NAME}/${MSC_NAME}-prod-config.git"
                SELF_SERVICE_REPO = "${GITHUB_URL}${ORGANIZATION_NAME}/self-service-app-ops-jenkins-jobs.git"
                GOM_REPO = "${GITHUB_URL}${ORGANIZATION_NAME}/git-org-manager.git"
            }
            steps {
                script {
                    dir('self') {
                        git credentialsId: 'sf-prod-config-self-service-serviceuser',
                        url: "${SELF_SERVICE_REPO}", branch: 'master'
                    }
                    dir('prod-config') {
                        git credentialsId: 'sf-prod-config-self-service-serviceuser',
                        url: "${PROD_CONFIG_REPO}", branch: 'master'
                    }
                    dir('git-org-manager') {
                        git credentialsId: 'sf-prod-config-self-service-serviceuser',
                       url: "${GOM_REPO}", branch: 'master'
                    }
                }
            }
        }
        stage("Validate Parameters") {
            steps {
                script {
                    wrap([$class: 'BuildUser']) {
                        env.BUILD_USER_ID = env.BUILD_USER_ID ?: "auto"
                    }
                    if (!ImageTag) {
                        error("Image Tag must be set.")
                    }
                    if (!ImageRepository) {
                        error("ImageRepository must be set.")
                    }
                }
            }
        }
        stage("Is the manifest files present") {
            environment {
                prodKustomizeYaml = "../prod-config/${DC_CHOICE}/${ENV_CHOICE}/kustomization.yaml"
            }
            steps {
                script {
                    container("sf-k8s-python") {
                        withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                            dir("release-operations") {
                                sh "python3 repo_check.py ${prodKustomizeYaml} ${MSC_NAME} ${ENV_CHOICE}"
                            }
                        }
                    }
                }
            }
        }
        stage("Is user having access admin/write for -dev-config repo?") {
            steps {
                script {
                    container("sf-k8s-python") {
                        dir("git-org-manager/src") {
                            withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                                sh "python3 gom.py repo --org-name=sf-k8s --org-token=$GITHUB_TOKEN --triggered-by=$BUILD_USER_ID has-access --ID=$BUILD_USER_ID --names=write,admin --repo-name=${DEV_REPO}"
                            }
                        }
                    }
                }
            }
        }
        stage("Does Docker Image exists?") {
            environment {
                DOCKERCRED = credentials('sfhcm-admin')
            }
            steps {
                script {
                    container("docker") {
                        try {
                            // Insecure flag set due to lack of SAP Certificates in "Docker" Docker image
                            sh "docker login --username ${DOCKERCRED_USR} --password ${DOCKERCRED_PSW} ${ImageArtifactory}"
                            sh "docker manifest inspect --insecure ${ImageArtifactory}/${ImageRepository}:${IMAGE_TAG}"
                       } catch (Error) {
                            error("${ImageRepository}:${IMAGE_TAG} not available in ${ImageArtifactory}")
                        }
                    }
                }
            }
        }
        stage('Pull and push image') {
            environment {
                SOURCE_ARTIFACTORY = "sfhcm.docker.repositories.sap.ondemand.com"
                TARGET_ARTIFACTORY = "sf-docker-golden.common.repositories.cloud.sap/k8s/qa/trunk"
                protocol = "https://"
                IMAGE_SVC = "${MSC_NAME}-svc"
            }
	        steps {
                script {
                    env.SOURCE_CREDENTIAL = getArtifactoryCredential(artifactoryCredentialsMaps, SOURCE_ARTIFACTORY)
                    env.TARGET_CREDENTIAL = getArtifactoryCredential(artifactoryCredentialsMaps, TARGET_ARTIFACTORY)
                    container('docker') {
                        docker.withRegistry(protocol + SOURCE_ARTIFACTORY, SOURCE_CREDENTIAL) {
                            sh "docker pull $SOURCE_ARTIFACTORY/$IMAGE_REPO:$IMAGE_TAG"
                            sh "docker tag $SOURCE_ARTIFACTORY/$IMAGE_REPO:$IMAGE_TAG $TARGET_ARTIFACTORY/$IMAGE_SVC:$IMAGE_TAG"
                        }
                        docker.withRegistry(protocol + TARGET_ARTIFACTORY, TARGET_CREDENTIAL) {
                            sh "docker push $TARGET_ARTIFACTORY/$IMAGE_SVC:$IMAGE_TAG"
                        }
                    }
                }
            }
        }
        stage("Does Release Tag exists?") {
            environment {
                imageTagWithV = "v${params.ImageTag}"
            }
            steps {
                script {
                    container("sf-k8s-python") {
                        dir("git-org-manager/src") {
                            withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                                flag = false
                                try {
                                    sh "python3 gom.py repo --org-name=sf-k8s --org-token=$GITHUB_TOKEN --triggered-by=$BUILD_USER_ID tag-exists --ID=${IMAGE_TAG} --repo-name=${DEV_REPO}"
                               } catch (Exception) {
                                    println("${IMAGE_TAG} not available in GIT ..Checking further with V")
                                    flag = true
                                }
                                if (flag == true) {
                                    try {
                                        sh "python3 gom.py repo --org-name=sf-k8s --org-token=$GITHUB_TOKEN --triggered-by=$BUILD_USER_ID tag-exists --ID=${imageTagWithV} --repo-name=${DEV_REPO}"
                                        IMAGE_TAG = imageTagWithV
                                } catch (Exception) {
                                        error("${imageTagWithV} not available in GIT")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        stage("GIT Push") {
            environment {
                GIT_DEV_URL = "${GITHUB_URL}${ORGANIZATION_NAME}/${MSC_NAME}-dev-config/base/?ref="
                prodKustomizeYaml = "../prod-config/${DC_CHOICE}/${ENV_CHOICE}/kustomization.yaml"
            }
            steps {
                script {
                    container("sf-k8s-python") {
                        withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                            dir("release-operations") {
                                sh "python3 update_prod_config.py ${IMAGE_TAG} ${prodKustomizeYaml} ${GIT_DEV_URL}"
                            }
                        }
                    }
                }
            }
        }
        stage("GIT Commit") {
            environment {
                GIT_PUSH_REPO = "github.tools.sap/${ORGANIZATION_NAME}/${MSC_NAME}-prod-config.git"
            }
            steps {
                script {
                    dir("prod-config") {
                        withCredentials([usernamePassword(credentialsId: "${GITHUB_CREDENTIAL_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                            sh script: 'git config user.email "jenkinsCICD@sap.com"'
                            sh script: "git config user.name ${GITHUB_CREDENTIAL_NAME}"
                            sh script: "git commit -a -m '$BUILD_USER_ID promoted the tag ${IMAGE_TAG}'", label: "Set Commit"
                            sh script: "git push https://${GITHUB_USER}:${GITHUB_TOKEN}@${GIT_PUSH_REPO}", label: "GIT push by $BUILD_USER_ID"
                        }
                    }
                }
            }
        }
        stage('ArgoCD Sync') {
            environment {
                ARGOCD_CREDS = credentials('argocd-cli')
                ARGOCD_REPO = "${MSC_NAME}-${ENV_CHOICE}-app"
                ARGOCD_SERVER = "argocd.sc25k8scl01.cksdc25.c.eu-de-1.cloud.sap"
            }
            steps {
                container('curl') {
                    sh 'curl -k -o /usr/local/bin/argocd https://argo.cksdc25.c.eu-de-1.cloud.sap/download/argocd-linux-amd64'
                    sh 'chmod +x /usr/local/bin/argocd'
                    sh "argocd login ${ARGOCD_SERVER} --grpc-web --insecure --username ${ARGOCD_CREDS_USR} --password ${ARGOCD_CREDS_PSW}"
                    sh "argocd app sync ${ARGOCD_REPO} --timeout 100 --prune"
                    sh "argocd app wait ${ARGOCD_REPO} --timeout 300"
                }
            }
        }
    }
}
