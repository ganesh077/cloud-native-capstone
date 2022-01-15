pipeline {
  agent any

  environment {
    AWS_DEFAULT_REGION = "us-east-1"
    PROJECT_NAME       = "cloud-native-capstone"
  }

  options {
    timestamps()
  }

  stages {
    stage('Setup Python') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '. .venv/bin/activate && pytest --junitxml=pytest-report.xml'
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'pytest-report.xml'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          env.IMAGE_TAG = env.BUILD_NUMBER ?: "dev"
          env.IMAGE_REPO = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_DEFAULT_REGION}.amazonaws.com/${env.PROJECT_NAME}"
          env.IMAGE_URI = "${env.IMAGE_REPO}:${env.IMAGE_TAG}"
        }
        sh 'docker build -t ${IMAGE_URI} .'
      }
    }

    stage('Push Image to ECR') {
      steps {
        sh '''
          aws ecr describe-repositories --repository-names ${PROJECT_NAME} >/dev/null 2>&1 || \
            aws ecr create-repository --repository-name ${PROJECT_NAME}
          aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
            docker login --username AWS --password-stdin ${IMAGE_REPO}
          docker push ${IMAGE_URI}
        '''
      }
    }

    stage('Terraform Plan & Apply') {
      steps {
        dir('terraform') {
          sh '''
            terraform init -input=false
            terraform plan -input=false -out=tfplan -var container_image_tag=${IMAGE_TAG}
            terraform apply -input=false -auto-approve tfplan
          '''
        }
      }
    }
  }
}
