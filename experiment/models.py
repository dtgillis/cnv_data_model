from django.db import models


class SampleManager(models.Manager):

    def create_sample_model(self, sample_name, bam_file, xt2_sample):
        sample = self.create(sample_name=sample_name, bam_file=bam_file, xt2_sample=xt2_sample)
        return sample


class Sample(models.Model):

    sample_name = models.CharField(max_length=100)
    bam_file = models.CharField(max_length=200)
    xt2_sample = models.BooleanField()
    objects = SampleManager()

    class Meta:
        unique_together = ('sample_name', 'bam_file')

    def __unicode__(self):
        if not self.xt2_sample:
            return self.sample_name + '-non-xt2'
        else:
            return self.sample_name + '-xt2'


class PoolManager(models.Manager):

    def create_pool(self, sample, pool_name):
        pool = self.create(sample=sample, pool_name=pool_name)
        return pool


class SampleGroup(models.Model):

    sample = models.ForeignKey(Sample)
    pool_name = models.CharField(max_length=100)
    objects = PoolManager()

    def __unicode__(self):
        return self.pool_name


class SoftwareManager(models.Manager):

    def create_software(self, software_name, extra_params):
        software = self.create(software_name=software_name, extra_params=extra_params)
        return software


class Software(models.Model):

    software_name = models.CharField(max_length=50)
    extra_params = models.TextField()
    objects = SoftwareManager()

    def __unicode__(self):
        return self.software_name + ":" + self.extra_params


class ChromosomeManager(models.Manager):

    def create_chromosome(self, chromosome_name, alternate_name):
        chromosome = self.create(chromosome_name=chromosome_name, alternate_name=alternate_name)
        return chromosome


class Chromosome(models.Model):

    chromosome_name = models.CharField(max_length=25)
    alternate_name = models.CharField(max_length=10)
    objects = ChromosomeManager()

    def __unicode__(self):
        return self.chromosome_name


class GenomeIntervalManager(models.Manager):

    def create_interval(self, chromosome, start, end):
        interval = self.create(chromosome=chromosome, start=start, end=end)
        return interval


class GenomeInterval(models.Model):

    chromosome = models.ForeignKey(Chromosome)
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    objects = GenomeIntervalManager()

    class Meta:
        unique_together = ('chromosome', 'start', 'end')

    def __unicode__(self):

        return "{0:s}:{1:d}-{2:d)".format(self.chromosome.__unicode__(), self.start, self.end)
