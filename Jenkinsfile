import org.apache.commons.httpclient.*
import org.apache.commons.httpclient.methods.multipart.*
import org.apache.commons.httpclient.methods.GetMethod
import org.apache.commons.httpclient.methods.PostMethod
import org.apache.commons.httpclient.methods.PutMethod
import org.apache.commons.httpclient.cookie.CookiePolicy
import groovy.json.*
import groovy.sql.Sql

def priceList=[:]
          
pipeline {
  agent {
    kubernetes {
      label 'k8s'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: some-label-value
spec:
  containers:
  - name: google
    image: google-api:latest 
    imagePullPolicy: Never
    env:
    - name: SAMPLE_RANGE_NAME
      value: "Kabum!A1:B2000"
    - name: SAMPLE_SPREADSHEET_ID
      value: "1oVEfoO179xnFzdndFHmwTb0Jo2xViEmZcyXmMZyLjEI"
    - name: WRITE_RANGE_NAME
      value: "Kabum"    
    command:
    - cat
    tty: true
"""
    }
  }
  //parameters {
       //choice(name: 'URL',  choices: ['https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo=148902','https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo=95217'], description: 'Loja que explode;')
       //text(name: 'URL', defaultValue: 'https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo=148902', description: 'Loja que explode;')
  //}  
  
  stages{
    //stage('docker_run'){
    //    steps{
    //        sh 'docker run --rm hello-world'
    //    }
    //}  
    stage('GetListToScrap') {
      steps {
        container('google') {
          sh """
             cp -rf /usr/src/app/* ./ 
             python app.py 1 > listToScrap.txt 
             cat listToScrap.txt 
          """
        }        
      }
    }    
    stage('Scraping') {
      steps {
        //sh "ls -la ./"
        script {
          def output = readFile('listToScrap.txt').trim()
          def outList = output.split(',').collect{it as String}
          println outList
          outList.each{
             println " scraping url: ${it}"  
             def html = processScraping(it)   
             (description, price) = transformHTML(html)
             priceList.put(description, price)
          }
        }        
      }
    }
    stage('Saving') {
      steps {
        container('google') {
            script{
                priceList.each { description, price ->
                    sh """
                     echo \"${price}\" 
                     echo \"${description}\"
                     python app.py 2 \"${price}\" \"${description}\"                
                    """
                }
            }
        }        
      }
    }    
  }
}
def processScraping(url){
    def httpClient = new HttpClient()
    def getUrl = new GetMethod(url)
    getUrl.getParams().setCookiePolicy(CookiePolicy.IGNORE_COOKIES)
    httpClient.executeMethod(getUrl)
    def html = getUrl.getResponseBodyAsString()
    return html
}
def transformHTML(String HTML) {
    def description=HTML.findAll(/=\W\w+det">(.+)/)[0].findAll(/>(.*)</)[0]
    def price=HTML.findAll(/avista-cm">(.+),\d+/)[0].findAll(/(\d+\.?\d+\,?\d+)/)[0]
    
    println description
    println price
    return [description, price]
}

