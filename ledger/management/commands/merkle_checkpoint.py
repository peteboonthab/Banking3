
from django.core.management.base import BaseCommand, CommandError
from ledger.merkle import MerkleTreeService


class Command(BaseCommand):
    help = "Create or verify a Merkle checkpoint"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["create", "verify"],
            help="Choose whether to create or verify a checkpoint",
        )
        parser.add_argument(
            "--id",
            type=int,
            help="Checkpoint ID to verify",
        )

    def handle(self, *args, **options):
        service = MerkleTreeService()
        action = options["action"]

        if action == "create":
            try:
                checkpoint = service.save_checkpoint()
            except ValueError as error:
                raise CommandError(str(error))

            self.stdout.write(
                self.style.SUCCESS(
                    f"Checkpoint created. ID: {checkpoint.id}, "
                    f"Records: {checkpoint.record_count}, "
                    f"Root: {checkpoint.root_hash}"
                )
            )

        elif action == "verify":
            checkpoint_id = options["id"]

            if checkpoint_id is None:
                raise CommandError(
                    "Please provide a checkpoint ID using --id."
                )

            try:
                valid = service.verify_checkpoint(checkpoint_id)
            except Exception as error:
                raise CommandError(str(error))

            if valid:
                self.stdout.write(
                    self.style.SUCCESS("Checkpoint verified successfully.")
                )
            else:
                self.stdout.write(
                    self.style.ERROR("Checkpoint verification failed.")
                )
