from storages.backends.s3boto3 import S3Boto3Storage

storage_class = S3Boto3Storage


class CustomerStorage(storage_class):
    file_overwrite = False
    # 重複名前毎計数する
    counts = {}

    def get_alternative_name(self, file_root, file_ext):
        if file_root not in self.counts:
            self.counts[file_root] = 1
        new_file_name = (
            file_root + "_" + str(self.counts[file_root]) + file_ext
        )
        self.counts[file_root] += 1
        return new_file_name
