from django.db import models


class Link(models.Model):
    link = models.CharField("Link", max_length=200)
    descricao = models.CharField("Descrição", max_length=100)
    ordem = models.PositiveSmallIntegerField("Ordem", null=True, blank=True)
    cor = models.PositiveSmallIntegerField("Cor")

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ["ordem"]

    def __str__(self):
        return self.descricao
