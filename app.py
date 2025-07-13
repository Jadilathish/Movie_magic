from flask import Flask
import boto3
from app.routes import bp as routes_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(routes_bp)

# AWS Configuration
AWS_REGION = 'us-east-1'  # Change to your region
DYNAMODB_TABLE = 'MovieMagic_Users' # Change to your table name
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:975050261480:Moviemagic:e94516c9-5888-4def-8678-504b5accbd45' # Change to your SNS topic ARN

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns = boto3.client('sns', region_name=AWS_REGION)

# Pass AWS clients to routes
app.config['DYNAMODB_TABLE'] = dynamodb.Table(DYNAMODB_TABLE)
app.config['SNS_CLIENT'] = sns
app.config['SNS_TOPIC_ARN'] = SNS_TOPIC_ARN

if __name__ == '__main__':
    app.run(debug=True)
