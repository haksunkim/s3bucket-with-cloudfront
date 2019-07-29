# s3bucket-with-cloudfront
This NPM package provides AWS CDK Construct, S3BucketWithCloudFront.

The S3BucketWithCloudFront construct will create S3Bucket with CloudFront
to server webpage to public.

To use this package, add dependency into package.json file as below.
```json
{
  "dependencies": {
    ...,
    "s3bucket-with-cloudfront": "haksunkim/s3bucket-with-cloudfront#<branch-name>",
    ...
  }
}
```

Then you need to run NPM command to make this package installed, and built.
```npm
npm install
npm run build
```
As this package will be installed from GitHub repository, the `npm run build`
is necessary to make the S3BucketWithCloudFront construct available.

Script below is an example of how the Construct can be used to create
- S3Bucket with CloudFront Origin Access Identity
- S3Bucket Policy allowing read access
- CloudFront configured to serve files from S3 bucket

```typescript
import cdk = require('@aws-cdk/core');
import { S3BucketWithCloudFront } from 's3bucket-with-cloudfront';

export class FlightInformationCdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const solutionNamingPrefix = 'solution-name';
    const s3BucketWithCloudFront = new S3BucketWithCloudFront(
        this,
        'S3BucketWithCloudFront',
        {
          applicationName: solutionNamingPrefix,
          defaultRootObject: 'index.html',
          errorConfigurations: [
            {
              errorCode: 404,
              responseCode: 200,
              errorCachingMinTtl: 300,
              responsePagePath: '/index.html'
            },{
              errorCode: 403,
              responseCode: 200,
              errorCachingMinTtl: 300,
              responsePagePath: '/index.html'
            }
          ]
        }
    );
  }
}

```
