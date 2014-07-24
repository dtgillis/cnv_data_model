from django.db import models
import experiment.models as exp
# Create your models here.


class CNVSChipManager(models.Manager):
    def create_cnv_chip_call(self, sample_name, chromosome, start, end, cn_state):
        cnv_chip_call = self.create(
            sample_name=sample_name, chrmosome=chromosome, start=start, end=end, cnstate=cn_state)
        return cnv_chip_call


class CNVChipCall(models.Model):

    sample_name = models.CharField(max_length=100)
    chromosome = models.ForeignKey(exp.Chromosome)
    start = models.IntegerField()
    end = models.IntegerField()
    cn_state = models.IntegerField()


class CNVSoftwareCallManager(models.Manager):

    def create_cnv_software_call(self, sample_group, chromosome, start, end, cn_state):
        cnv_software_call = self.create(
            sample_group=sample_group, chromosome=chromosome, start=start, end=end, cn_state=cn_state)
        return cnv_software_call


class CNVSoftwareCall(models.Model):

    sample_group = models.ForeignKey(exp.SampleGroup)
    chromosome = models.ForeignKey(exp.Chromosome)
    start = models.IntegerField()
    end = models.IntegerField()
    cn_state = models.IntegerField()


