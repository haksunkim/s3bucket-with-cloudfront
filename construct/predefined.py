from aws_cdk import core
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_cloudfront import (
    CfnCloudFrontOriginAccessIdentity,
    CloudFrontWebDistribution,
    HttpVersion,
    SourceConfiguration,
    S3OriginConfig,
    CloudFrontAllowedMethods,
    Behavior,
    CfnDistribution,
    ViewerProtocolPolicy,
    PriceClass,
)
from aws_cdk.aws_iam import ArnPrincipal


class S3BucketWithCloudFront(core.Construct):
    def __init__(self, scope: core.Construct, id: str, solution_name: str, **kwargs):
        super().__init__(scope, id)

        web_application_bucket = Bucket(
            self,
            id='WebApplicationBucket',
            bucket_name="%s-webapp" % solution_name,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        cf_origin_access_identity = CfnCloudFrontOriginAccessIdentity(
            self,
            id='CloudFrontOriginAccessIdentity',
            cloud_front_origin_access_identity_config={
                "comment": "OAI for %s" % web_application_bucket.bucket_name,
            }
        )

        cf_distribution = CloudFrontWebDistribution(
            self,
            id='CloudFrontWebDistribution',
            default_root_object=kwargs.get('default_root_object', 'index.html'),
            enable_ip_v6=False,
            http_version=HttpVersion.HTTP2,
            origin_configs=[
                SourceConfiguration(
                    s3_origin_source=S3OriginConfig(
                        s3_bucket_source=web_application_bucket,
                        origin_access_identity_id=cf_origin_access_identity.ref,
                    ),
                    behaviors=[
                        Behavior(
                            allowed_methods=CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
                            forwarded_values=CfnDistribution.ForwardedValuesProperty(
                                query_string=True,
                                cookies={
                                    "forward": "none",
                                }
                            ),
                            default_ttl=core.Duration.seconds(0),
                            is_default_behavior=True,
                        )
                    ],
                )
            ],
            viewer_protocol_policy=ViewerProtocolPolicy.ALLOW_ALL,
            error_configurations=kwargs.get('error_configurations', [
                CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=200,
                    error_caching_min_ttl=300,
                    response_page_path='/index.html',
                ),
                CfnDistribution.CustomErrorResponseProperty(
                    error_code=403,
                    response_code=200,
                    error_caching_min_ttl=300,
                    response_page_path='/index.html',
                ),
            ]),
            price_class=PriceClass.PRICE_CLASS_ALL,
        )

        web_application_bucket.grant_read(
            identity=ArnPrincipal(
                "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity %s" % cf_origin_access_identity.ref)
        )

        core.CfnOutput(
            self,
            id='CloudFrontDistrubutionDNS',
            value=cf_distribution.domain_name,
        )

        core.CfnOutput(
            self,
            id='DefaultRootObject',
            value=kwargs.get('default_root_object', 'index.html'),
        )

        core.CfnOutput(
            self,
            id='S3Bucket',
            value=web_application_bucket.bucket_domain_name,
        )
