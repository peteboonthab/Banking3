
import json
from pymerkle import InmemoryTree
from .models import AuditLog, MerkleCheckpoint


class MerkleTreeService:

    def serialize_audit_log(self, record):
        audit_data = {
            "id": record.id,
            "user_id": record.user_id,
            "action": record.action,
            "object_type": record.object_type,
            "object_id": record.object_id,
            "details": record.details,
            "ip_address": record.ip_address,
            "created_at": record.created_at.isoformat(),
        }

        return json.dumps(
            audit_data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

    def build_merkle_tree(self):
        tree = InmemoryTree(algorithm="sha256")

        audit_logs = list(
            AuditLog.objects.order_by("created_at", "id")
        )

        for record in audit_logs:
            tree.append_entry(self.serialize_audit_log(record))

        return tree, audit_logs

    def save_checkpoint(self):
        tree, audit_logs = self.build_merkle_tree()

        if not audit_logs:
            raise ValueError("Cannot save a checkpoint with no audit records.")

        return MerkleCheckpoint.objects.create(
            root_hash=tree.get_state().hex(),
            record_count=len(audit_logs),
        )

    def verify_checkpoint(self, checkpoint_id):
        checkpoint = MerkleCheckpoint.objects.get(id=checkpoint_id)
        tree, audit_logs = self.build_merkle_tree()

        if not audit_logs:
            return False

        if len(audit_logs) != checkpoint.record_count:
            return False

        return tree.get_state().hex() == checkpoint.root_hash

