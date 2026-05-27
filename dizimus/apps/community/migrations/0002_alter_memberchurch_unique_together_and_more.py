# Reescrito manualmente.
# Motivo: users/0006 deletou users_memberchurch antes que esta migration
# pudesse renomeá-la. Solução: criar community_memberchurch do zero.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_move_memberchurch_from_users'),
        ('users', '0006_delete_memberchurch'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # ── Banco: cria a tabela do zero ─────────────────────────────────
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        CREATE TABLE "community_memberchurch" (
                            "id"        bigserial    NOT NULL PRIMARY KEY,
                            "role"      varchar(30)  NOT NULL,
                            "status"    varchar(20)  NOT NULL,
                            "joined_at" timestamptz  NOT NULL,
                            "left_at"   timestamptz  NULL,
                            "member_id" bigint       NOT NULL
                                REFERENCES "users_member" ("id")
                                ON DELETE CASCADE
                                DEFERRABLE INITIALLY DEFERRED,
                            "church_id" bigint       NOT NULL
                                REFERENCES "users_church" ("id")
                                ON DELETE CASCADE
                                DEFERRABLE INITIALLY DEFERRED,
                            CONSTRAINT "unique_member_church"
                                UNIQUE ("member_id", "church_id")
                        );
                        CREATE INDEX "community_m_member__208e90_idx"
                            ON "community_memberchurch" ("member_id", "church_id");
                        CREATE INDEX "community_m_church__b1cb72_idx"
                            ON "community_memberchurch" ("church_id", "role");
                        CREATE INDEX "community_m_church__14504b_idx"
                            ON "community_memberchurch" ("church_id", "status");
                    """,
                    reverse_sql='DROP TABLE IF EXISTS "community_memberchurch";',
                ),
            ],
            # ── Estado: sincroniza o Django com o banco ───────────────────────
            state_operations=[
                migrations.AlterModelTable(
                    name='memberchurch',
                    table=None,  # volta ao padrão → community_memberchurch
                ),
                migrations.AlterUniqueTogether(
                    name='memberchurch',
                    unique_together={('member', 'church')},
                ),
                migrations.AddIndex(
                    model_name='memberchurch',
                    index=models.Index(
                        fields=['member', 'church'],
                        name='community_m_member__208e90_idx',
                    ),
                ),
                migrations.AddIndex(
                    model_name='memberchurch',
                    index=models.Index(
                        fields=['church', 'role'],
                        name='community_m_church__b1cb72_idx',
                    ),
                ),
                migrations.AddIndex(
                    model_name='memberchurch',
                    index=models.Index(
                        fields=['church', 'status'],
                        name='community_m_church__14504b_idx',
                    ),
                ),
            ],
        ),
    ]
