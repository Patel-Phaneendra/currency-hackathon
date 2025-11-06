pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
        ALPHAVANTAGE_API_KEY = credentials('alphavantage-api-key')  // API key stored in Jenkins credentials
    }
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/Patel-Phaneendra/currency-hackathon.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t currency-converter:python-currency-docs .'
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run --rm -v $PWD:/app -e ALPHAVANTAGE_API_KEY=${ALPHAVANTAGE_API_KEY} currency-converter:python-currency-docs'
                }
            }
        }
        stage('Check and Display Docs Files') {
            steps {
                script {
                    def txtPath = 'out/api_docs.txt'
                    def htmlPath = 'out/api_docs.html'
                    def txtExists = fileExists(txtPath)
                    def htmlExists = fileExists(htmlPath)
                    if (txtExists && htmlExists) {
                        echo "API docs generated successfully."
                        echo readFile(txtPath)
                        echo readFile(htmlPath)
                    } else {
                        if (!txtExists) { echo "api_docs.txt is missing in the out folder." }
                        if (!htmlExists) { echo "api_docs.html is missing in the out folder." }
                        error('Required docs files missing!')
                    }
                }
            }
        }
        stage('Commit and Push Output Files') {
            steps {
                script {
                    sh 'git config user.email "jenkins@localhost"'
                    sh 'git config user.name "Jenkins CI"'
                    sh 'git add out/api_docs.txt out/api_docs.html'
                    sh '''
                        if ! git diff --cached --quiet; then
                            git commit -m "Add/Update docs from Jenkins pipeline"
                            git push origin HEAD:main
                        else
                            echo "No changes to commit."
                        fi
                    '''
                }
            }
        }
    }
}
