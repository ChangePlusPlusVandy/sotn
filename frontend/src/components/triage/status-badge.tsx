import { cn } from "@/lib/utils";
import { STATUS_LABELS, type InquiryStatus } from "./inquiry-labels";

const STATUS_COLORS: Record<InquiryStatus, string> = {
  new: "bg-sotn-blue-mid/15 text-sotn-blue-dark",
  needs_review: "bg-sotn-yellow-mid/15 text-sotn-yellow-dark",
  assigned: "bg-sotn-purple-mid/15 text-sotn-purple-dark",
  contacted: "bg-sotn-grey-mid/15 text-sotn-grey-dark",
  referred: "bg-sotn-green-mid/15 text-sotn-green-dark",
  closed: "bg-sotn-magenta-mid/15 text-sotn-magenta-dark",
};

export const StatusBadge = ({ status }: { status: InquiryStatus }) => {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-sm leading-4 whitespace-nowrap",
        STATUS_COLORS[status],
      )}
    >
      {STATUS_LABELS[status]}
    </span>
  );
};
