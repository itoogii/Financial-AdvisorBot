import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

if (!process.env.S3_ENDPOINT) {
  throw new Error("S3_ENDPOINT is not set");
}

if (!process.env.S3_ACCESS_KEY_ID) {
  throw new Error("S3_ACCESS_KEY_ID is not set");
}

if (!process.env.S3_SECRET_ACCESS_KEY) {
  throw new Error("S3_SECRET_ACCESS_KEY is not set");
}

if (!process.env.S3_BUCKET_NAME) {
  throw new Error("S3_BUCKET_NAME is not set");
}

const s3Client = new S3Client({
  endpoint: process.env.S3_ENDPOINT,
  region: process.env.S3_REGION,
  credentials: {
    accessKeyId: process.env.S3_ACCESS_KEY_ID!,
    secretAccessKey: process.env.S3_SECRET_ACCESS_KEY!,
  },
  useDualstackEndpoint: false,
  forcePathStyle: true,
});

export async function put(file: Buffer, fileName: string) {
  const response = await s3Client.send(
    new PutObjectCommand({
      Body: file,
      Bucket: process.env.S3_BUCKET_NAME,
      Key: fileName,
    }),
  );
  return response;
}
