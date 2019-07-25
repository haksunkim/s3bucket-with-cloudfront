import {Construct, Duration, RemovalPolicy} from '@aws-cdk/core';
import {Bucket} from "@aws-cdk/aws-s3";
import {
    CfnCloudFrontOriginAccessIdentity, CfnDistribution,
    CloudFrontAllowedMethods,
    CloudFrontWebDistribution,
    HttpVersion, PriceClass, ViewerProtocolPolicy
} from "@aws-cdk/aws-cloudfront";
import {ArnPrincipal} from "@aws-cdk/aws-iam";
import CustomErrorResponseProperty = CfnDistribution.CustomErrorResponseProperty;

export interface S3BucketWithCloudFrontProp {
    applicationName: string;
    defaultRootObject?: string;
    errorConfigurations?: CustomErrorResponseProperty[];
}

export class S3BucketWithCloudFront extends Construct {
    constructor(scope: Construct, id: string, props: S3BucketWithCloudFrontProp) {
        super(scope, id);

        // by default, the defaultRootObject is set to 'index.html'
        if (props.defaultRootObject == null) props.defaultRootObject = 'index.html';

        const solutionNamingPrefix = props.applicationName;

        const webApplicationBucket = new Bucket(this, 'WebApplicationBucket', {
            bucketName: solutionNamingPrefix + '-webapp',
            removalPolicy: RemovalPolicy.DESTROY
        });

        const cfOriginAccessIdentity = new CfnCloudFrontOriginAccessIdentity(this, 'CloudFrontOriginAccessIdentity', {
            cloudFrontOriginAccessIdentityConfig: {
                comment: 'OAI for ' + webApplicationBucket.bucketName
            }
        });

        const cfDistribution = new CloudFrontWebDistribution(this, 'CloudFrontDistribution', {
            defaultRootObject: props.defaultRootObject,
            enableIpV6: false,
            httpVersion: HttpVersion.HTTP2,
            originConfigs: [
                {
                    s3OriginSource: {
                        originAccessIdentityId: cfOriginAccessIdentity.ref,
                        s3BucketSource: webApplicationBucket
                    },
                    behaviors: [
                        {
                            allowedMethods: CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            forwardedValues: {
                                queryString: true,
                                cookies: {
                                    forward: "none"
                                }
                            },
                            defaultTtl: Duration.seconds(0),
                            isDefaultBehavior: true
                        }
                    ]
                }
            ],
            viewerProtocolPolicy: ViewerProtocolPolicy.ALLOW_ALL,
            errorConfigurations: props.errorConfigurations,
            priceClass: PriceClass.PRICE_CLASS_ALL
        });

        webApplicationBucket.grantRead({
            grantPrincipal: new ArnPrincipal('arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ' + cfOriginAccessIdentity.ref)
        });
    }
}
