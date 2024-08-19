from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.devtools import Codepipeline, Codebuild
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAMRole
from diagrams.aws.general import User

with Diagram("Refined AWS EKS Architecture", show=False):
    users = User("Users")

    with Cluster("AWS Cloud"):
        eks_cluster = EKS("EKS Cluster")
        
        with Cluster("VPC"):
            elb = ELB("Load Balancer")
            eks_service = EKS("Service")
            
            with Cluster("Kubernetes Components"):
                app_deploy = EKS("App Deployment")
                app_pod = EKS("App Pod")
                db_statefulset = RDS("DB StatefulSet")
                db_pod = EKS("DB Pod")
                app_deploy - app_pod
                db_statefulset - db_pod

            with Cluster("Monitoring"):
                cloudwatch = Cloudwatch("CloudWatch")
                cloudwatch - eks_cluster

            with Cluster("CI/CD"):
                codepipeline = Codepipeline("CodePipeline")
                codebuild = Codebuild("CodeBuild")
                codepipeline - codebuild
                codebuild - eks_cluster

    s3 = S3("Persistent Storage")

    users >> elb >> eks_service
    eks_service >> app_deploy
    eks_service >> db_statefulset
    cloudwatch >> Edge(color="firebrick", style="dashed") >> app_deploy
    cloudwatch >> Edge(color="firebrick", style="dashed") >> db_statefulset
    codepipeline >> Edge(color="blue", style="dotted") >> app_deploy
    codepipeline >> Edge(color="blue", style="dotted") >> db_statefulset
    db_pod >> Edge(color="green", style="solid") >> s3
