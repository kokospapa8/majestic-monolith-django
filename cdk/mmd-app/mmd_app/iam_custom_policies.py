import aws_cdk.aws_iam as iam


def get_policy_ecs_server_task_policy():

    # Creating new custom Policies
    ecs_server_policy = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=[
            "s3:*",
            "ssm:*",
            "cloudwatch:*",
            "kms:*",
            "logs:*",
            "lambda:*",
            "secretsmanager:*",
            "ssm:*",
            "events:PutEvents",
        ],
    )

    return ecs_server_policy


def get_policy_ecs_execution_policy():

    # Creating new custom Policies
    ecs_execution_policy = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=[
            "s3:*",
            "ssm:*",
            "cloudwatch:*",
            "kms:*",
            "logs:*",
            "lambda:*",
            "secretsmanager:*",
            "ssm:*",
        ],
    )

    return ecs_execution_policy


def get_policy_bastion_instance():
    bastion_Instance = iam.PolicyStatement(
        resources=["*"],
        sid="VisualEditor0",
        actions=["s3:*", "kms:*", "secretsmanager:*"],
    )

    return bastion_Instance


def get_policy_code_deploy():
    bastion_Instance = iam.PolicyStatement(
        resources=["*"],
        effect=iam.Effect.ALLOW,
        actions=[
            "ecs:RegisterTaskDefinition",
            "iam:PassRole",
            "ecs:DescribeServices",
            "codedeploy:GetDeploymentGroup",
            "codedeploy:CreateDeployment",
            "codedeploy:GetDeployment",
            "codedeploy:GetDeploymentConfig",
            "codedeploy:RegisterApplicationRevision",
        ],
    )

    return bastion_Instance
