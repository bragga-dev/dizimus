# class ChurchAffiliationRequest(models.Model):

#     class Status(models.TextChoices):
#         PENDING = "pending", "Pendente"
#         ACCEPTED = "accepted", "Aceito"
#         REJECTED = "rejected", "Recusado"
#         EXPIRED = "expired", "Expirado"
#         CANCELED = "canceled", "Cancelado"

#     class RequestType(models.TextChoices):
#         INVITE = "invite", "Convite"
#         REQUEST = "request", "Solicitação"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)

#     # quem iniciou
#     from_church = models.ForeignKey(
#         Church,
#         on_delete=models.CASCADE,
#         related_name="sent_affiliation_requests",
#     )

#     # quem recebe
#     to_church = models.ForeignKey(
#         Church,
#         on_delete=models.CASCADE,
#         related_name="received_affiliation_requests",
#     )

#     request_type = models.CharField(
#         max_length=20,
#         choices=RequestType.choices,
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=Status.choices,
#         default=Status.PENDING,
#     )

#     code = models.CharField(
#         max_length=12,
#         unique=True,
#         null=True,
#         blank=True,
#     )

#     message = models.TextField(
#         null=True,
#         blank=True,
#     )

#     expires_at = models.DateTimeField(
#         null=True,
#         blank=True,
#     )

#     created_at = models.DateTimeField(auto_now_add=True)