
from django.test import TestCase

from ledger.models import AuditLog, MerkleCheckpoint
from ledger.merkle import MerkleTreeService


class MerkleTreeServiceTests(TestCase):

    def setUp(self):
        # Create the service used by each test.
        self.service = MerkleTreeService()

        # Create an audit record for testing.
        self.audit_log = AuditLog.objects.create(
            action="TRANSFER",
            object_type="LedgerEntry",
            object_id="1",
            details={"amount": "100.00"},
            ip_address="127.0.0.1",
        )

    def test_checkpoint_is_created(self):
        checkpoint = self.service.save_checkpoint()

        self.assertIsInstance(checkpoint, MerkleCheckpoint)
        self.assertEqual(checkpoint.record_count, 1)
        self.assertTrue(checkpoint.root_hash)

    def test_checkpoint_verifies_without_changes(self):
        checkpoint = self.service.save_checkpoint()

        result = self.service.verify_checkpoint(checkpoint.id)

        self.assertTrue(result)

    def test_verification_fails_when_audit_record_is_added(self):
        checkpoint = self.service.save_checkpoint()

        # Add another audit record after the checkpoint.
        AuditLog.objects.create(
            action="TRANSFER",
            object_type="LedgerEntry",
            object_id="2",
            details={"amount": "250.00"},
            ip_address="127.0.0.1",
        )

        result = self.service.verify_checkpoint(checkpoint.id)

        self.assertFalse(result)

    def test_checkpoint_stores_correct_record_count(self):
        checkpoint = self.service.save_checkpoint()

        self.assertEqual(
            checkpoint.record_count,
            AuditLog.objects.count(),
        )
