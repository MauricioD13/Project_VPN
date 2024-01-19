import boto3

def security_group_create(ec2):
    # Create security group allowing SSH access
    response = ec2.create_security_group(
        GroupName="ssh-access", Description="Security group with SSH access"
    )

    security_group_id = response["GroupId"]
    print("Security group ID: ", security_group_id)
    # Authorize SSH access
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            }
        ],
    )

    return security_group_id

def create_vpc():
    ec2 = boto3.client("ec2")

    # Create VPC
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    try:
        # Create subnet
        subnet = ec2.create_subnet(CidrBlock="10.0.1.0/24", VpcId=vpc_id)
        subnet_id = subnet["Subnet"]["SubnetId"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidSubnet.Conflict":
            print("Subnet already exists, using existing one")
            subnet_id = "subnet-5678efgh"  # Existing subnet
        else:
            raise

    # Create internet gateway
    igw = ec2.create_internet_gateway()

    try:
        ec2.attach_internet_gateway(
            InternetGatewayId=igw["InternetGateway"]["InternetGatewayId"], VpcId=vpc_id
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "Gateway.NotAttached":
            print("IGW already attached, continuing...")
        else:
            raise

    # Create route table and add public route
    route_table = ec2.create_route_table(VpcId=vpc_id)
    route_table_id = route_table["RouteTable"]["RouteTableId"]
    ec2.create_route(
        RouteTableId=route_table_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=igw_id
    )

    # Associate subnet with route table
    ec2.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)

    print(f"VPC ID: {vpc_id}")
    print(f"Subnet ID: {subnet_id}")
