FROM apache/spark:3.5.1-scala2.12-java17-python3-r-ubuntu

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    boto3==1.28.57 \
    pandas==2.1.1 \
    pyarrow==13.0.0 \
    numpy==1.24.3

# Hadoop AWS connector (S3 / MinIO support)
RUN curl -L \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    -o /opt/spark/jars/hadoop-aws-3.3.4.jar

# AWS SDK bundle (required dependency)
RUN curl -L \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    -o /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar

RUN mkdir -p /opt/spark-app && chmod 777 /opt/spark-app

WORKDIR /opt/spark-app

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

USER spark