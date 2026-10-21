
from django.db import migrations


def create_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return

    schema_editor.execute("""
        CREATE TRIGGER ledger_entry_after_insert
        AFTER INSERT ON ledger_ledgerentry
        BEGIN
            INSERT INTO ledger_ledgerentryaudit
                (ledger_entry_id, activity, recorded_at)
            VALUES
                (NEW.id, 'INSERT', CURRENT_TIMESTAMP);
        END;
    """)

    schema_editor.execute("""
        CREATE TRIGGER ledger_entry_after_update
        AFTER UPDATE ON ledger_ledgerentry
        BEGIN
            INSERT INTO ledger_ledgerentryaudit
                (ledger_entry_id, activity, recorded_at)
            VALUES
                (NEW.id, 'UPDATE', CURRENT_TIMESTAMP);
        END;
    """)

    schema_editor.execute("""
        CREATE TRIGGER ledger_entry_after_delete
        AFTER DELETE ON ledger_ledgerentry
        BEGIN
            INSERT INTO ledger_ledgerentryaudit
                (ledger_entry_id, activity, recorded_at)
            VALUES
                (OLD.id, 'DELETE', CURRENT_TIMESTAMP);
        END;
    """)


def remove_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return

    schema_editor.execute(
        "DROP TRIGGER IF EXISTS ledger_entry_after_insert;"
    )
    schema_editor.execute(
        "DROP TRIGGER IF EXISTS ledger_entry_after_update;"
    )
    schema_editor.execute(
        "DROP TRIGGER IF EXISTS ledger_entry_after_delete;"
    )


class Migration(migrations.Migration):

    dependencies = [
    ('ledger', '0005_ledgerentryaudit'),
]

    operations = [
        migrations.RunPython(create_triggers, remove_triggers),
    ]
