import BaseModal from "./BaseModal";

export default function ProjectModal({
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
      title="Projects"
    >
      <h3>Vasuki</h3>
      <p>Personal Intelligence OS</p>

      <h3>Janani</h3>
      <p>Discipline Engine</p>

      <h3>MW.AI</h3>
      <p>AI Systems for Businesses</p>
    </BaseModal>
  );
}
