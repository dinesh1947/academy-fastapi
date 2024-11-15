pipeline {
     agent any
    stages {
	       stage("Checkout code"){
		   steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/dev'], [name: '*/staging'], [name: '*/prod']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'git@github.com:stellardevteam/fastapi_academy_forumias_api_python.git']]])
            }
		   }
		   
        stage("Deployment") {
            steps {
                script {
                    def branch = env.BRANCH_NAME
                    if (branch == "dev") {
					 echo "Deploying to dev environment"
					 sh '/home/ubuntu/scripts/fastapiforumiasdevserver/sshapidev.sh'
					 sh 'sudo scp -i /home/ubuntu/keys/academyforumiasdevserver/devapiacadamy.pem -r /var/lib/jenkins/workspace/fastapi_academy_forumias_com_dev/academy/* ubuntu@52.1.147.59:/home/ubuntu/public_html/fastapidevacademy.forumias.com'
           sh '/home/ubuntu/scripts/fastapidevacademy.forumias.com/apidev_sshtorestartsupervisor.sh'
					} else if (branch == "staging") {
                     echo "Deploying to staging environment, Lol we don't have staging branch for this job so no deployement"		  
                     } else if (branch == "prod") {
					 echo "Deploying to prod environment"
                     // Below is to Deploy on Mumbai region server
                   //  sh '/home/ubuntu/scripts/prodapiacademyserver/mumbai/sshapiprod.sh'
                  // sh 'sudo scp -i /home/ubuntu/keys/prodapiacademyserver/prodapiacademy.pem -r /var/lib/jenkins/workspace/ackend_academy_forumias_com_prod/academy/* ubuntu@65.0.161.122:/home/ubuntu/public_html/prodapiacademy'
                  //  sh '/home/ubuntu/scripts/prodapiacademyserver/mumbai/apiprod_sshtorestartsupervisor.sh'
                    } else {
                        echo "Branch not recognized so no any further action"
                    }
                }
        }
			
       }
}
}