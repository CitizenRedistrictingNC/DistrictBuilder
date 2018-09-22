from troposphere import Output, Parameter, Ref, Template
import troposphere.ec2 as ec2

t = Template(Description='An ec2 instance, with a security group, and EIP')

name = t.add_parameter(
    Parameter('Name', Description='Name of EC2 stack', Type='String'))
sshLocation = t.add_parameter(
    Parameter(
        'SSHLocation',
        Type='String',
        Default='0.0.0.0/0',
        MinLength=9,
        MaxLength=18,
        AllowedPattern=
        '(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})',
        ConstraintDescription=
        'must be a valid IP CIDR range of the form x.x.x.x/x.'))
keyName = t.add_parameter(
    Parameter(
        'KeyName',
        Description=
        'Name of an existing EC2 KeyPair to enable SSH access to the instances',
        Type='String',
        ConstraintDescription='must be the name of an existing EC2 KeyPair.'))

securityGroup = ec2.SecurityGroup('InstanceSecurityGroup')
securityGroup.GroupDescription = 'SSH and HTTP Access'
securityGroup.SecurityGroupIngress = [
    ec2.SecurityGroupRule(
        IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp=Ref(sshLocation)),
    ec2.SecurityGroupRule(
        IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp='0.0.0.0/0'),
    ec2.SecurityGroupRule(
        IpProtocol='tcp', FromPort=443, ToPort=443, CidrIp='0.0.0.0/0'),
]

instance = ec2.Instance(
    "ec2instance", ImageId="ami-07917569e2c4a2b6a", InstanceType="t2.micro")
instance.SecurityGroups = [Ref(securityGroup)]
instance.KeyName = Ref(keyName)
instance.BlockDeviceMappings = [
    ec2.BlockDeviceMapping(
        DeviceName='/dev/sda1', Ebs=ec2.EBSBlockDevice(VolumeSize=30))
]
instance.Tags = [ec2.Tag('Name', Ref(name))]

ipAddress = ec2.EIP('IPAddress')
ipAssociation = ec2.EIPAssociation(
    'EIPAssociation', InstanceId=Ref(instance), EIP=Ref(ipAddress))

t.add_resource(instance)
t.add_resource(securityGroup)
t.add_resource(ipAddress)
t.add_resource(ipAssociation)
t.add_output(
    Output(
        'InstanceId',
        Description='InstanceId of the newly created EC2 instance',
        Value=Ref(instance)))
t.add_output(
    Output(
        'InstanceIPAddress',
        Description='IP address of the newly created EC2 instance',
        Value=Ref(ipAddress)))

print(t.to_json())
