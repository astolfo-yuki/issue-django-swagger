class Channel(models.Model):
    name = models.CharField(max_length=1024, db_index=True, unique=True)

class Cluster(models.Model):
    name = models.CharField(max_length=1024, db_index=True, unique=True)
    channel = models.ForeignKey(
        Channel, on_delete=models.SET_NULL, null=True
    )

class rule(models.Model):
    app_id = models.CharField(max_length=32, db_index=False)
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, related_name="rules", null=True
    )
    name = models.CharField(max_length=1024, db_index=True)
    partition = models.CharField(max_length=128, db_index=True)

    objects = ruleManager()

    class Meta:
        verbose_name_plural = "rules"
        unique_together = ("app_id", "cluster")
        indexes = [models.Index(fields=["app_id", "cluster"])]

    def __str__(self):
        return self.full_path
