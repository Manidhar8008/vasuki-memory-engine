import BaseModal from "./BaseModal";

export default function EvidenceModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  return (
    <BaseModal
      open={open}
      onClose={onClose}
      title="Evidence"
    >
      <ul>
        <li>595 Documents</li>
        <li>42648 Entities</li>
        <li>1239 Evidence Records</li>
        <li>165 Timeline Events</li>
      </ul>
    </BaseModal>
  );
}
