import setuptools

with open("README.md", "r'") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3bucket-with-cloudfront",
    version="0.0.1",
    author="Haksun Kim",
    author_email="itpro@haksunkim.com",
    description="AWS CDK Construct for S3Bucket with CloudFront",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haksunkim/s3bucket-with-cloudfront",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
